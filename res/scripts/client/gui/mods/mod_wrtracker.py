# -*- coding: utf-8 -*-

from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework import g_entitiesFactories, ScopeTemplates, ViewSettings, ViewTypes
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.app_loader import g_appLoader
from gui.app_loader.settings import APP_NAME_SPACE
from gui.shared import events, EVENT_BUS_SCOPE, g_eventBus
from wrtracker_stats import AccountStats

WR_TRACKER_VIEW = 'KALAS_WR_TRACKER_VIEW'
SWF_NAME = 'kalas.wrtracker.WrTrackerView.swf'


def _win_rate(wins, battles):
    return 0.0 if battles <= 0 else round(float(wins) * 100.0 / battles, 2)


def _wins_to_target(wins, battles, target):
    if battles <= 0 or target >= 100.0:
        return 0
    if float(wins) * 100.0 / battles >= target:
        return 0
    t = target / 100.0
    n = int(max(0.0, (t * battles - wins) / (1.0 - t)))
    while float(wins + n) * 100.0 / (battles + n) < target:
        n += 1
    return n


class WRTrackerView(View):
    def __init__(self, *args, **kwargs):
        super(WRTrackerView, self).__init__(*args, **kwargs)
        self._stats = AccountStats()
        print('[WRTracker] View __init__')

    def _populate(self):
        super(WRTrackerView, self)._populate()
        print('[WRTracker] View populated, flashObject=%r' % self.flashObject)
        self._update()

    def _dispose(self):
        print('[WRTracker] View disposed')
        self._stats = None
        super(WRTrackerView, self)._dispose()

    def _update(self):
        result = self._stats.update()
        print('[WRTracker] stats result=%r' % (result,))
        if not result:
            self.as_setData('', '', '', '')
            return
        wins, battles = result
        wr = _win_rate(wins, battles)
        half = (int(wr * 2.0) + 1) / 2.0
        whole = int(wr) + 1
        self.as_setData(
            '%.2f' % wr,
            '%.1f' % half,
            '%d' % _wins_to_target(wins, battles, half),
            '%.1f|%d|%d' % (whole, _wins_to_target(wins, battles, whole), battles)
        )

    def as_setData(self, wr, half_target, half_wins, whole_data):
        print('[WRTracker] as_setData(%r, %r, %r, %r)' %
              (wr, half_target, half_wins, whole_data))
        if self.flashObject is not None:
            self.flashObject.as_setData(wr, half_target, half_wins, whole_data)


def _load_view():
    try:
        app = g_appLoader.getDefLobbyApp()
        print('[WRTracker] getDefLobbyApp=%r' % (app,))
        if app is not None:
            app.loadView(SFViewLoadParams(WR_TRACKER_VIEW))
            print('[WRTracker] loadView requested')
            return True
    except Exception as exc:
        print('[WRTracker] loadView failed: %s' % exc)
    return False


def _on_app_initialized(event):
    if event.ns != APP_NAME_SPACE.SF_LOBBY:
        return
    print('[WRTracker] SF_LOBBY initialized')
    _load_view()


def setup():
    settings = ViewSettings(
        WR_TRACKER_VIEW,
        WRTrackerView,
        SWF_NAME,
        ViewTypes.WINDOW,
        None,
        ScopeTemplates.DEFAULT_SCOPE
    )
    g_entitiesFactories.addSettings(settings)
    g_eventBus.addListener(
        events.AppLifeCycleEvent.INITIALIZED,
        _on_app_initialized,
        EVENT_BUS_SCOPE.GLOBAL
    )

    # The mod can be imported after the lobby INITIALIZED event has already fired.
    # In that case the event listener alone never creates the view.
    _load_view()


setup()
print('[WRTracker] prototype initialized')
