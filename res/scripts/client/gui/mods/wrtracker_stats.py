# -*- coding: utf-8 -*-

from helpers import dependency
from skeletons.gui.shared import IItemsCache


class AccountStats(object):
    itemsCache = dependency.descriptor(IItemsCache)

    def __init__(self):
        self.wins = 0
        self.battles = 0

    def update(self):
        try:
            dossier = self.itemsCache.items.getAccountDossier()
            if dossier is None:
                return False
            total = dossier.getTotalStats()
            self.battles = int(total.getBattlesCount() or 0)
            self.wins = int(total.getWinsCount() or 0)
            return self.battles > 0
        except Exception as exc:
            print('[WRTracker] stats update failed: %s' % exc)
            return False
