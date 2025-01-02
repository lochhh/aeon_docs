from pathlib import Path

import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from sphinx.application import Sphinx
from sphinx.locale import __
from sphinx.util import logging
from sphinx.util.osutil import copyfile, ensuredir
from sphinx.util.typing import ExtensionMetadata

logger = logging.getLogger(__name__)


class WorkflowDirective(Directive):
    """A directive to include a Bonsai workflow image.

    The directive takes the path of a .bonsai workflow file as its content,
    and looks for the corresponding .svg file to include as an image.
    As an optional argument, an alt text for the image can be provided.

    The directive will copy the workflow image to the _images folder.

    If the builder output is html, it will also copy the Bonsai source file
    into the _workflows folder so it can be fetched by copy button scripts.
    """

    required_arguments = 0
    optional_arguments = 0
    has_content = True
    option_spec = {"alt": directives.unchanged}

    def run(self):
        try:
            # Raise an error if the directive does not have contents.
            self.assert_has_content()
            srcpath = Path(directives.uri(self.content[0]))
            imgpath = srcpath.with_suffix(".svg")
            # Create a container to contain the workflow image
            self.options["uri"] = str(imgpath)
            image_node = nodes.image(rawsource=self.block_text, **self.options)
            container_node = nodes.container(classes=["workflow"])
            container_node += image_node
            # Make sure the workflow source file exists and has .bonsai extension
            abs_srcpath = (
                Path(self.state.document["source"]).parent / srcpath
            ).resolve()
            if not abs_srcpath.exists() or abs_srcpath.suffix != ".bonsai":
                logger.warning(__("Invalid workflow file: %s"), srcpath)
            # Make sure the workflow image exists
            abs_imgpath = (
                Path(self.state.document["source"]).parent / imgpath
            ).resolve()
            if not abs_imgpath.exists():
                logger.warning(
                    __("Could not find workflow image: %s [%s]"),
                    imgpath,
                    abs_imgpath,
                )
            # Copy workflow image to _images folder
            imagedir = self.state.document.settings.env.app.builder.outdir / "_images"
            destpath = imagedir / imgpath.name
            ensuredir(imagedir)
            copyfile(abs_imgpath, destpath)
            # Copy workflow file to _workflows folder when output is html
            if self.state.document.settings.env.app.builder.format == "html":
                abs_workflowdir = (
                    self.state.document.settings.env.app.builder.outdir / "_workflows"
                )
                abs_workflowpath = abs_workflowdir / srcpath.name
                ensuredir(abs_workflowdir)
                copyfile(abs_srcpath, abs_workflowpath)
        except Exception as exc:
            logger.warning(__("Could not fetch workflow image: %s [%s]"), imgpath, exc)
        finally:
            return [container_node]


def setup(app: Sphinx) -> ExtensionMetadata:
    app.add_directive("workflow", WorkflowDirective)
    return {
        "version": sphinx.__display_version__,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
