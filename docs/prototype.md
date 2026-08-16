# WRTracker prototype

Target client: Мир Танков 1.44.0.7794.

The prototype intentionally targets the lobby/hangar only. It reads the account dossier through `IItemsCache`, then sends four values to a Scaleform SWF:

1. current WR;
2. next `.50` target;
3. wins to that target;
4. next whole-percent target, wins to it, and battle count.

The supplied `tv.lebwa.gunmarks_1.4.00.mtmod` was inspected as a reference for package layout. Its lobby/battle SWFs and Python bytecode confirm the general Python + Scaleform architecture. Its UI is not copied into WRTracker.

The open WoT source mirror also exposes the account dossier path used by the lobby/profile code: `itemsCache.items.getAccountDossier().getTotalStats()`, including `getBattlesCount()`; the prototype pairs that with `getWinsCount()`.

## Current limitation

The repository contains the AS3 source but not a compiled SWF yet. A local Apache Royale/Flex SWF compiler is required to build `kalas.wrtracker.WrTrackerView.swf`. This environment does not have such a compiler installed and cannot download one. Therefore this commit is a source prototype, not yet a drop-in `.mtmod` release.

Once the SWF is compiled, place it at `res/gui/flash/kalas.wrtracker.WrTrackerView.swf`, compile the Python source with the client's Python 2.7, and package `meta.xml` plus `res/` as `.mtmod`.
