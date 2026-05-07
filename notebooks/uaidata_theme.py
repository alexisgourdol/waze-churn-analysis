"""
uai data — Seaborn / Matplotlib Custom Theme
=============================================
Derived from the uai data design system (uaidata.io).

Usage
-----
    import uaidata_theme          # apply on import
    # or call explicitly:
    uaidata_theme.apply()

    import seaborn as sns
    import matplotlib.pyplot as plt

    # Use the palette directly:
    sns.barplot(data=df, x="category", y="value",
                palette=uaidata_theme.PALETTE)

    # Use a single-hue sequential palette:
    sns.heatmap(data=pivot, cmap=uaidata_theme.cmap_sequential())

    # Restore matplotlib defaults:
    uaidata_theme.reset()
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns


# ── Design tokens ──────────────────────────────────────────────────────────────

# Backgrounds & surfaces
BG          = "#FAF9F6"   # warm off-white — figure background
SURFACE     = "#F2F1ED"   # cards / axes background
SURFACE_2   = "#F5F4F0"   # alternate section bg
BORDER      = "#E5E4DF"   # all dividers, grid lines, spines

# Text
TEXT        = "#1C1C1A"   # primary — titles, tick labels
TEXT_MUTED  = "#6B6A66"   # secondary — axis labels, annotations

# Accent (primary data colour)
ACCENT      = "#F59E0B"   # amber
ACCENT_DARK = "#D97706"   # amber hover / darker shade

# Fixed-dark surface
SURFACE_INVERT = "#1C1C1A"

# ── Categorical palette ────────────────────────────────────────────────────────
# Ordered by visual salience: lead with amber, then indigo, teal, pink,
# then two supporting neutrals derived from brand tones.

PALETTE = [
    "#F59E0B",   # amber   — accent / primary series
    "#6366F1",   # indigo  — project-2
    "#0D9488",   # teal    — project-3
    "#EC4899",   # pink    — project-4
    "#1C1C1A",   # near-black — strong contrast series
    "#6B6A66",   # warm grey  — supporting / secondary series
    "#FCD34D",   # light amber (lighter variant for extended palettes)
    "#A5B4FC",   # light indigo
]

# ── Sequential colormaps ───────────────────────────────────────────────────────

def cmap_sequential(base: str = ACCENT, name: str = "uaidata_seq") -> mcolors.LinearSegmentedColormap:
    """Single-hue sequential colourmap from near-white to `base`."""
    return mcolors.LinearSegmentedColormap.from_list(
        name, [BG, base]
    )

def cmap_diverging(
    low: str = "#6366F1",
    high: str = ACCENT,
    mid: str = BORDER,
    name: str = "uaidata_div",
) -> mcolors.LinearSegmentedColormap:
    """Diverging colourmap (indigo → neutral → amber)."""
    return mcolors.LinearSegmentedColormap.from_list(
        name, [low, mid, high]
    )


# ── RC params ─────────────────────────────────────────────────────────────────

def _build_rc() -> dict:
    return {
        # ── Figure
        "figure.facecolor":        BG,
        "figure.edgecolor":        BG,
        "figure.dpi":              150,
        "figure.autolayout":       True,

        # ── Axes
        "axes.facecolor":          SURFACE,
        "axes.edgecolor":          BORDER,
        "axes.linewidth":          1.0,
        "axes.grid":               True,
        "axes.grid.axis":          "y",
        "axes.spines.top":         False,
        "axes.spines.right":       False,
        "axes.spines.left":        False,
        "axes.spines.bottom":      True,
        "axes.labelcolor":         TEXT_MUTED,
        "axes.labelpad":           8,
        "axes.titlecolor":         TEXT,
        "axes.titleweight":        "700",
        "axes.titlepad":           14,
        "axes.titlesize":          14,
        "axes.labelsize":          11,
        "axes.prop_cycle":         mpl.cycler(color=PALETTE),

        # ── Grid
        "grid.color":              BORDER,
        "grid.linewidth":          1.0,
        "grid.alpha":              1.0,
        "grid.linestyle":          "-",

        # ── Ticks
        "xtick.color":             TEXT_MUTED,
        "ytick.color":             TEXT_MUTED,
        "xtick.labelsize":         10,
        "ytick.labelsize":         10,
        "xtick.major.size":        0,
        "ytick.major.size":        0,
        "xtick.minor.size":        0,
        "ytick.minor.size":        0,
        "xtick.bottom":            False,
        "ytick.left":              False,

        # ── Lines & markers
        "lines.linewidth":         2.0,
        "lines.markersize":        6,
        "patch.edgecolor":         "none",
        "patch.linewidth":         0,

        # ── Legend
        "legend.frameon":          True,
        "legend.framealpha":       1.0,
        "legend.facecolor":        BG,
        "legend.edgecolor":        BORDER,
        "legend.fontsize":         10,
        "legend.title_fontsize":   10,

        # ── Font — DM Sans if installed, else a clean system sans-serif
        "font.family":             "sans-serif",
        "font.sans-serif":         ["DM Sans", "Inter", "Helvetica Neue",
                                    "Arial", "DejaVu Sans"],
        "text.color":              TEXT,

        # ── Savefig
        "savefig.facecolor":       BG,
        "savefig.edgecolor":       BG,
        "savefig.dpi":             200,
        "savefig.bbox":            "tight",
        "savefig.pad_inches":      0.3,
    }


# ── Public API ─────────────────────────────────────────────────────────────────

def apply() -> None:
    """Apply the uai data theme globally."""
    mpl.rcParams.update(_build_rc())
    sns.set_theme(
        style="white",       # seaborn style base (we override via rc)
        rc=_build_rc(),
    )
    # Register custom colourmaps so they're accessible by name
    for _cm in [cmap_sequential(), cmap_diverging()]:
        try:
            mpl.colormaps.register(_cm, force=True)
        except AttributeError:
            # matplotlib < 3.5 fallback
            plt.register_cmap(cmap=_cm)


def reset() -> None:
    """Restore matplotlib/seaborn defaults."""
    mpl.rcdefaults()
    sns.reset_defaults()


# ── Auto-apply on import ───────────────────────────────────────────────────────
apply()
