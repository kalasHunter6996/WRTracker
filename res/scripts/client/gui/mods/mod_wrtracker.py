# -*- coding: utf-8 -*-
from gui.Scaleform.framework.entities.View import View
from gui.Scaleform.framework import g_entitiesFactories, ScopeTemplates, ViewSettings
from gui.Scaleform.framework.managers.loaders import SFViewLoadParams
from gui.shared import events, EVENT_BUS_SCOPE, g_eventBus
from gui.app_loader.settings import APP_NAME_SPACE
from helpers import dependency
from skeletons.gui.app_loader import IAppLoader
from wrtracker_stats import AccountStats

WR_TRACKER_VIEW = 'KALAS_WR_TRACKER_VIEW'
SWF_NAME = 'kalas.wrtracker.WrTrackerView.swf'


def _get_app_loader():
    return dependency.instance(IAppLoader)


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
                self.as_setData('', '', '', '')
                return
            wins, battles = result
            wr = round(float(wins) * 100.0 / battles, 2)
            half = (int(wr * 2.0) + 1) / 2.0
            whole = int(wr) + 1
            self.as_setData('%.2f' % wr, '%.1f' % half,
                            str(self._wins_to_target(wins, battles, half)),
                            '%d|%d|%d' % (whole,
                                           self._wins_to_target(wins, battles, whole),
                                           battles))
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
        print('[WRTracker] as_setData(%r, %r, %r, %r)' %
              (wr, half_target, half_wins, whole_data))
        if self.flashObject is not None:
            self.flashObject.as_setData(wr, half_target, half_wins, whole_data)


def _load_view():
    try:
        app_loader = _get_app_loader()
        print('[WRTracker] appLoader=%r' % app_loader)
        app = app_loader.getDefLobbyApp()
        print('[WRTracker] getDefLobbyApp=%r' % app)
        if app is not None:
            app.loadView(SFViewLoadParams(WR_TRACKER_VIEW))
            print('[WRTracker] loadView requested')
    except Exception as exc:
        print('[WRTracker] loadView failed: %s' % exc)


def _on_app_initialized(event):
    if event.ns == APP_NAME_SPACE.SF_LOBBY:
        print('[WRTracker] SF_LOBBY initialized')
        _load_view()


def setup():
    # ViewTypes.WINDOW is unavailable in this client branch; 0 is the
    # corresponding window view type used by the target framework API.
    settings = ViewSettings(WR_TRACKER_VIEW, WRTrackerView, SWF_NAME,
                            0, None, ScopeTemplates.DEFAULT_SCOPE)
    g_entitiesFactories.addSettings(settings)
    g_eventBus.addListener(events.AppLifeCycleEvent.INITIALIZED,
                           _on_app_initialized, EVENT_BUS_SCOPE.GLOBAL)
    _load_view()


setup()
print('[WRTracker] prototype initialized')
