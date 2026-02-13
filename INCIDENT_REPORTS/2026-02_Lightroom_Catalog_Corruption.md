-------------
Lightroom Classic Export Failure — Deep Troubleshooting & Salvage Write-up
-------------

**Problem Summary**

Lightroom Classic entered a failure state where JPEG exports stalled indefinetely for almost all images in a specific shoot, despite:

* No visible "Not Responding" state
* Minimal CPU usage (0-3%, Activity Monitor)
* Stable export destinations (internal(desktop) + external SSD)
* No filename collisions
* Valid file permissions
* No GPU acceleration involvement
* No apparent catalog corruption per SQLite integrity checks (`PRAGMA integrity_check;`)

Only ***one specific image*** consistently exported successfully; all others hung the export export pipeline.


**Initial Hypotheses**

I evaluated common Lightroom failure vectors first:

1. Disk I/O failure
    * Tested export to Desktop (internal disk file destination)
    * Tested export to external SSD
    * Result: ❌ ruled out

2. Filename collisions
    * Lightroom did not warn of overwrites
    * Unique filenames confirmed
    * Result: ❌ ruled out

3. GPU acceleration
    * GPU disabled in Lighroom config settings
    * Result: ❌ ruled out

4. Camera Raw cache
    * Cache purged
    * CameraRaw directory reset
    * Result: ❌ ruled out

5. Permissions / extended attributes
    * File permissions verified
    * xattr -c applied to RAW files
    * Result: ❌ ruled out

6. Preset/watermark/metadata export
    * No export presets 
    * Default metadata tagging setting
    * No watermark
    * Result: ❌ ruled out

**Key Observation That Changed the Direction**

A ***brand-new empty catalog*** could:
    * Import a failing RAW 
    * Export it successfully

Meanwhile:
    * The ***original catalog*** could not export *any* image except one
    * Even unrelated photos failed to export

This strongly indicated ***catalog-level corruption or deadlock***, not RAW data corruption. 


**Catalog Forensics (SQLite-Level)**

Since Lightroom catalogs are SQLite-backed, we validated the catalog itself:

SQL

`PRAGMA integrity_check;`

Result:

`ok`

So:

* No structural corruption
* No broken B-trees
* No missing pages

However, Lightroom uses ***multiple internal storage systems***, not just the .lrcat file:

* SQLite DB
* WAL / SHM
* .lrdata blobs
* Preview databases
* Internal edit state graphs

This meant that corruption could exist ***above SQLite validity***, inside Lightroom's internal edit or render pipeline.

**Additional Clues**

* Lightroom generated a new *Previews.lr-data* on launch after renaming existing file as backup
* Export still failed
* Saving metadata to XMP (to preserve recent edits) failed with:
code
`Unknown file I/O error (14)`
* Export stalled *even after Develop reset*
* Catalog migration/import failed

These point to:
* A broken internal state machine
* Possibly a poisoned render queue or edit stack reference
* Not recoverable via reset, cache purge, or catalog migration

**Critical Constraints**

* *Edits were never written to XMP sidecars*
* All edits *existed only inside the catalog*
* Backups predated renaming/relinking work (and subsequent recent edits)
* Goal was *salvage finished edits*, not full edit history across unrelated photos

This ruled out:

* Rebuilding from backups
* Re-importing RAWs and syncing metadata

**Nuclear Salvage Strategy**

At this stage, I stopped "fixing Lightroom" and *switched to data extraction*

**Why Print-to-File worked**

The Print module:
* Uses a **different render pipeline** from Library / Develop
* Bypasses export queue logic
* Does not rely on the same metadata/write mechanis,s
* Can rasterize the *final rendered image* without touching catalog write paths

*Execution*

* Used Print module
* Printed to JPEG
* Successfully exported fully rendered images with edits intact

This produced:

* Flattened, final JPEGs (albeit with no edit history)
* But critically, **edits were preserved** with no dependency on the corrupted catalog state

**Post-Salvage Recovery Plan**

1. Create a fresh catalog (no import/migration -> failed)
2. Import salvaged JPEGs
3. Treat JPEGs as:
    * New "master finals"
    * Starting points for any further edits
4. Accept loss of:
    * RAW edit history
    * Parametric adjustability





