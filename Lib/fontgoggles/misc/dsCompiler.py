import os
import pickle
from fontTools.designspaceLib import DesignSpaceDocument
from fontTools.fontBuilder import FontBuilder
from fontTools.ttLib import TTFont, newTable
from fontTools import varLib


def compileMinimumFont(dsPath, ttFolder):
    doc = DesignSpaceDocument.fromfile(dsPath)
    doc.findDefault()

    for source in doc.sources:
        if source.layerName is None:
            ttPath = os.path.join(ttFolder, os.path.basename(source.path) + ".ttf")
            assert os.path.exists(ttPath)
            source.font = TTFont(ttPath, lazy=False)  # TODO: https://github.com/fonttools/fonttools/issues/1808

    assert doc.default.font is not None
    doc.default.font["name"] = newTable("name")  # This is the template for the VF, and needs a name table

    if any(s.layerName is not None for s in doc.sources):
        fb = FontBuilder(unitsPerEm=doc.default.font["head"].unitsPerEm)
        fb.setupGlyphOrder(doc.default.font.getGlyphOrder())
        fb.setupPost()  # This makes sure we store the glyph names
        font = fb.font
        for source in doc.sources:
            if source.font is None:
                source.font = font

    ttFont, masterModel, _ = varLib.build(doc, exclude=['MVAR', 'HVAR', 'VVAR', 'STAT'])

    with open(os.path.join(ttFolder, "masterModel.pickle"), "wb") as f:
        # Our client needs the masterModel, so we save a pickle.
        pickle.dump(masterModel, f)

    return ttFont


def compileMinimumFontToPath(dsPath, ttFolder, ttPath):
    ttFont = compileMinimumFont(dsPath, ttFolder)
    ttFont.save(ttPath, reorderTables=False)