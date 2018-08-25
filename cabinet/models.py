from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.db import models
from django.db.models import signals
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from cabinet.base import AbstractFile, DownloadMixin, ImageMixin, OverwriteMixin


if not hasattr(settings, "CABINET_FILE_MODEL"):
    settings.CABINET_FILE_MODEL = "cabinet.File"


def get_file_model():
    """
    Return the File model that is active in this project.
    """
    try:
        return apps.get_model(settings.CABINET_FILE_MODEL, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "CABINET_FILE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "CABINET_FILE_MODEL refers to model '%s'"
            " that has not been installed" % settings.CABINET_FILE_MODEL
        )


class Folder(models.Model):
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name=_("parent"),
        related_name="children",
    )
    name = models.CharField(_("name"), max_length=100)

    class Meta:
        ordering = ["name"]
        unique_together = [("parent", "name")]
        verbose_name = _("folder")
        verbose_name_plural = _("folders")

    def __str__(self):
        return self.name

    def ancestors(self):
        node = self
        while True:
            yield node
            if node.parent_id:
                node = node.parent
            else:
                break

    def clean(self):
        if (
            self.id
            and self.parent_id
            and (self.id in [node.id for node in self.parent.ancestors()])
        ):
            raise ValidationError({"parent": _("Loop detected.")})


class File(AbstractFile, ImageMixin, DownloadMixin, OverwriteMixin):
    FILE_FIELDS = ["image_file", "download_file"]

    caption = models.CharField(_("caption"), max_length=1000, blank=True)
    copyright = models.CharField(_("copyright"), max_length=1000, blank=True)

    class Meta(AbstractFile.Meta):
        swappable = "CABINET_FILE_MODEL"


@receiver(signals.post_delete, sender=File)
def delete_files(sender, instance, **kwargs):
    instance.delete_files()
