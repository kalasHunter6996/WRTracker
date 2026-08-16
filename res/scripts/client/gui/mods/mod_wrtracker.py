# -*- coding: utf-8 -*-
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


class WRTrackerView(View):
    def __init__(self, *args, **kwargs):
        super(WRTrackerView, self).__init__(*args, **kwargs)
        self._stats = AccountStats()
        print('[WRTracker] View __init__')

    def _populate(self):
        super(WRTrackerView, self)._populate()
        print('[WRTracker] View populated, flashObject=%r' % self.flashObject)
        self._update()

    def _update(self):
        try:
            result = self._stats.update()
            print('[WRTracker] stats result=%r' % (result,))
            if not result:
                return

            wins, battles = result
            wr = round(float(wins) * 100.0 / battles, 2)
            half = (int(wr * 2.0) + 1) / 2.0
            whole = int(wr) + 1
            self.as_setData(
                '%.2f' % wr,
                '%.1f' % half,
                str(self._wins_to_target(wins, battles, half)),
                '%d|%d|%d' % (
                    whole,
                    self._wins_to_target(wins, battles, whole),
                    battles
                )
            )
        except Exception as exc:
            print('[WRTracker] update failed: %s' % exc)

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
    if event.ns == APP_NAME_SPACE.SF_LOBBY:
        print('[WRTracker] SF_LOBBY initialized')
        _load_view(event)


def setup():
    settings = ViewSettings(
        WR_TRACKER_VIEW,
        WRTrackerView,
        SWF_NAME,
        WindowLayer.WINDOW,
        None,
        ScopeTemplates.VIEW_SCOPE
    )
    g_entitiesFactories.addSettings(settings)
    g_eventBus.addListener(
        events.AppLifeCycleEvent.INITIALIZED,
        _on_app_initialized,
        EVENT_BUS_SCOPE.GLOBAL
    )


setup()
print('[WRTracker] prototype initialized')
