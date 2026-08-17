# -*- coding: utf-8 -*-
import BigWorld
from frameworks.wulf import WindowLayer
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework import g_entitiesFactories, ScopeTemplates, ViewSettings
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared import events, EVENT_BUS_SCOPE, g_eventBus
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared.personality import ServicesLocator
from wrtracker_stats import AccountStats

WR_TRACKER_VIEW = 'KALAS_WR_TRACKER_VIEW'
SWF_NAME = 'kalas.wrtracker.WrTrackerView.swf'
REFRESH_INTERVAL = 5.0


class WRTrackerView(View):
    def __init__(self, *args, **kwargs):
        super(WRTrackerView, self).__init__(*args, **kwargs)
        self._stats = AccountStats()
        self._polls = 0
        self._polling = False
        self._refresh_scheduled = False
        print('[WRTracker] View __init__')

    def _populate(self):
        super(WRTrackerView, self)._populate()
        print('[WRTracker] View populated, flashObject=%r' % self.flashObject)
        self._force_visible()
        self._schedule_update(initial=True)

    def _dispose(self):
        print('[WRTracker] View dispose')
        self._refresh_scheduled = False
        self._polling = False
        super(WRTrackerView, self)._dispose()

    def _force_visible(self):
        try:
            self.flashObject.visible = True
            self.flashObject.alpha = 1.0
            self.flashObject.x = 30
            self.flashObject.y = 170
            self.flashObject.scaleX = 1.0
            self.flashObject.scaleY = 1.0
            print('[WRTracker] forced flashObject visible at x=30 y=170')
        except Exception as exc:
            print('[WRTracker] force visible failed: %s' % exc)

    def _schedule_update(self, initial=False):
        if self._refresh_scheduled or self.flashObject is None:
            return
        self._refresh_scheduled = True
        delay = 0.5 if initial else REFRESH_INTERVAL
        BigWorld.callback(delay, self._refresh)

    def _refresh(self):
        self._refresh_scheduled = False
        if self.flashObject is None:
            return
        self._force_visible()
        self._poll_stats()

    def _poll_stats(self):
        if self.flashObject is None:
            return
        self._polls += 1
        if self._update():
            self._polls = 0
        elif self._polls < 60:
            BigWorld.callback(1.0, self._poll_stats)
            self._polling = True
            return
        else:
            print('[WRTracker] stats polling timed out')
            self._polls = 0

        self._polling = False
        self._schedule_update()

    def _update(self):
        try:
            result = self._stats.update()
            print('[WRTracker] stats result=%r' % (result,))
            if not result:
                return False

            wins, battles = result
            if battles <= 0:
                print('[WRTracker] stats invalid: battles=%d wins=%d' % (battles, wins))
                return False

            raw_wr = float(wins) * 100.0 / battles
            wr = round(raw_wr, 2)
            half = (int(raw_wr * 2.0) + 1) / 2.0
            whole = int(raw_wr) + 1
            half_wins = self._wins_to_target(wins, battles, half)
            whole_wins = self._wins_to_target(wins, battles, whole)
            print('[WRTracker] battles=%d wins=%d winrate=%.2f halfTarget=%.1f halfWins=%d wholeTarget=%d wholeWins=%d' % (
                battles, wins, wr, half, half_wins, whole, whole_wins
            ))
            self.as_setData(
                '%.2f' % wr,
                '%.1f' % half,
                str(half_wins),
                '%d|%d|%d' % (whole, whole_wins, battles)
            )
            return True
        except Exception as exc:
            print('[WRTracker] update failed: %s' % exc)
            return False

    def _wins_to_target(self, wins, battles, target):
        if target >= 100.0 or float(wins) * 100.0 / battles >= target:
            return 0
        t = target / 100.0
        n = int(max(0.0, (t * battles - wins) / (1.0 - t)))
        while float(wins + n) * 100.0 / (battles + n) < target:
            n += 1
        return n

    def as_setData(self, wr, half_target, half_wins, whole_data):
        if self.flashObject is not None:
            self.flashObject.as_setData(wr, half_target, half_wins, whole_data)


_loaded = False


def _load_view(event=None):
    global _loaded
    if _loaded:
        return
    try:
        app = ServicesLocator.appLoader.getApp(APP_NAME_SPACE.SF_LOBBY)
        print('[WRTracker] lobby app=%r' % app)
        if app is None:
            return
        app.loadView(SFViewLoadParams(WR_TRACKER_VIEW))
        _loaded = True
        print('[WRTracker] loadView requested')
    except Exception as exc:
        print('[WRTracker] loadView failed: %s' % exc)


def _on_app_initialized(event):
    global _loaded
    if event.ns == APP_NAME_SPACE.SF_LOBBY:
        print('[WRTracker] SF_LOBBY initialized (loaded=%r)' % _loaded)
        _loaded = False
        _load_view(event)


def _on_app_destroyed(event):
    global _loaded
    if event.ns == APP_NAME_SPACE.SF_LOBBY:
        _loaded = False
        print('[WRTracker] SF_LOBBY destroyed; tracker will reload on next lobby init')


def setup():
    settings = ViewSettings(
        WR_TRACKER_VIEW,
        WRTrackerView,
        SWF_NAME,
        WindowLayer.TOP_WINDOW,
        None,
        ScopeTemplates.DEFAULT_SCOPE
    )
    g_entitiesFactories.addSettings(settings)
    g_eventBus.addListener(
        events.AppLifeCycleEvent.INITIALIZED,
        _on_app_initialized,
        EVENT_BUS_SCOPE.GLOBAL
    )
    g_eventBus.addListener(
        events.AppLifeCycleEvent.DESTROYED,
        _on_app_destroyed,
        EVENT_BUS_SCOPE.GLOBAL
    )


setup()
print('[WRTracker] prototype initialized')
