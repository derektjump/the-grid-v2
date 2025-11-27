"""
Digital Signage Models

This module defines the data models for the digital signage design and data management portal.

IMPORTANT: This app is NOT a signage player or live dashboard.
It is an INTERNAL DESIGN + DATA PORTAL where we:
  - Design screen content (HTML/CSS/JS)
  - Preview what screens will look like
  - Manage signage-related data
  - Upload and organize media assets (images/videos)
  - Copy final designs into ScreenCloud Playground

Models:
    - ScreenDesign: Design templates for signage screens (HTML/CSS/JS)
    - Playlist: Collections of screens to rotate through on devices
    - PlaylistItem: Individual screens within a playlist with ordering and duration
    - Device: Physical devices (Firesticks/TVs) that display signage content
    - MediaFolder: Folders for organizing media assets
    - MediaAsset: Images and videos for use in playlists
    - Screen: (DEPRECATED - kept for backward compatibility) Legacy screen model
    - SalesData: Tracks daily sales data by store and employee
    - KPI: Tracks key performance indicators including targets and actual sales
"""

from django.db import models
from django.core.validators import MinValueValidator, FileExtensionValidator
from django.utils.text import slugify
from decimal import Decimal
import uuid
import random
import string
import os


def generate_registration_code(length=6):
    """Generate a random alphanumeric registration code."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


class ScreenDesign(models.Model):
    """
    Screen Design Template Model

    Represents an internal design template for signage screens.
    This is where we design, preview, and manage HTML/CSS/JS code
    that will be copied into ScreenCloud Playground.

    This model is NOT for live playback - it's for design management only.
    """

    name = models.CharField(
        max_length=200,
        help_text="Descriptive name for this screen design (e.g., 'Sales Dashboard Q1')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier for this design"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of what this screen design displays and its purpose"
    )

    # Code fields - the actual design content
    html_code = models.TextField(
        blank=True,
        help_text="HTML code for the screen content"
    )

    css_code = models.TextField(
        blank=True,
        help_text="CSS code for styling the screen"
    )

    js_code = models.TextField(
        blank=True,
        help_text="JavaScript code for dynamic behavior"
    )

    # Design notes and metadata
    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this design (usage instructions, data sources, etc.)"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this design is actively being used"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Screen Design"
        verbose_name_plural = "Screen Designs"
        ordering = ['-updated_at']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_preview_url(self):
        """
        Get the preview URL for this screen design.

        Returns:
            str: Relative URL path for previewing this design
        """
        from django.urls import reverse
        return reverse('digital_signage:screen_design_preview', kwargs={'slug': self.slug})


def media_upload_path(instance, filename):
    """Generate upload path for media files: media/signage/<folder_slug>/<filename>"""
    if instance.folder:
        return f'signage/{instance.folder.slug}/{filename}'
    return f'signage/uncategorized/{filename}'


def thumbnail_upload_path(instance, filename):
    """Generate upload path for thumbnails: media/signage/thumbnails/<filename>"""
    return f'signage/thumbnails/{filename}'


class MediaFolder(models.Model):
    """
    Media Folder Model

    Organizes media assets into folders for easier management.
    Supports nested folders through parent relationship.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this folder"
    )

    name = models.CharField(
        max_length=200,
        help_text="Folder name (e.g., 'Store Promotions', 'Product Images')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier for this folder"
    )

    description = models.TextField(
        blank=True,
        help_text="Description of what this folder contains"
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text="Parent folder (for nested organization)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Media Folder"
        verbose_name_plural = "Media Folders"
        ordering = ['name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} / {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def asset_count(self):
        """Return the number of assets in this folder."""
        return self.assets.count()

    @property
    def full_path(self):
        """Return the full folder path (including parents)."""
        if self.parent:
            return f"{self.parent.full_path} / {self.name}"
        return self.name


class MediaAsset(models.Model):
    """
    Media Asset Model

    Represents an uploaded image or video file that can be used in playlists.
    """

    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
    ALLOWED_VIDEO_EXTENSIONS = ['mp4', 'webm', 'mov', 'avi']

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this media asset"
    )

    name = models.CharField(
        max_length=200,
        help_text="Display name for this media (e.g., 'Holiday Sale Banner')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier for this media"
    )

    description = models.TextField(
        blank=True,
        help_text="Description or notes about this media"
    )

    file = models.FileField(
        upload_to=media_upload_path,
        validators=[
            FileExtensionValidator(
                allowed_extensions=ALLOWED_IMAGE_EXTENSIONS + ALLOWED_VIDEO_EXTENSIONS
            )
        ],
        help_text="The image or video file"
    )

    asset_type = models.CharField(
        max_length=10,
        choices=ASSET_TYPE_CHOICES,
        help_text="Type of media asset (auto-detected from file extension)"
    )

    folder = models.ForeignKey(
        MediaFolder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assets',
        help_text="Folder this asset belongs to"
    )

    thumbnail = models.ImageField(
        upload_to=thumbnail_upload_path,
        null=True,
        blank=True,
        help_text="Thumbnail image (auto-generated for videos)"
    )

    # Media metadata
    duration_seconds = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration in seconds (for videos only)"
    )

    width = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Width in pixels"
    )

    height = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Height in pixels"
    )

    file_size = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="File size in bytes"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this asset is available for use"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Media Asset"
        verbose_name_plural = "Media Assets"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['asset_type', 'is_active']),
            models.Index(fields=['folder', '-created_at']),
        ]

    def __str__(self):
        return f"{self.name} ({self.asset_type})"

    def save(self, *args, **kwargs):
        """Auto-generate slug and detect asset type."""
        if not self.slug:
            self.slug = slugify(self.name)

        # Auto-detect asset type from file extension
        if self.file:
            ext = os.path.splitext(self.file.name)[1].lower().strip('.')
            if ext in self.ALLOWED_IMAGE_EXTENSIONS:
                self.asset_type = 'image'
            elif ext in self.ALLOWED_VIDEO_EXTENSIONS:
                self.asset_type = 'video'

        super().save(*args, **kwargs)

    @property
    def file_extension(self):
        """Return the file extension."""
        if self.file:
            return os.path.splitext(self.file.name)[1].lower().strip('.')
        return ''

    @property
    def file_size_display(self):
        """Return human-readable file size."""
        if not self.file_size:
            return 'Unknown'
        size = self.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    @property
    def dimensions_display(self):
        """Return dimensions as 'WxH' string."""
        if self.width and self.height:
            return f"{self.width}x{self.height}"
        return 'Unknown'

    def get_player_url(self):
        """Get the player URL for this media asset."""
        from django.urls import reverse
        return reverse('digital_signage:media_player', kwargs={'slug': self.slug})


class Screen(models.Model):
    """
    DEPRECATED: Legacy Screen model for ScreenCloud integration.

    This model was originally designed for live playback but is no longer
    the primary design management tool. Use ScreenDesign instead.

    Kept for backward compatibility with existing data and migrations.
    May be removed or repurposed in future versions.
    """

    # Layout type choices - extensible for future layouts
    LAYOUT_CHOICES = [
        ('test', 'Test Layout'),
        # Future layouts will be added here:
        # ('profit_by_location', 'Profit by Location'),
        # ('device_sales', 'Device Sales Dashboard'),
        # ('custom', 'Custom HTML/CSS/JS'),
    ]

    name = models.CharField(
        max_length=200,
        help_text="Descriptive name for this screen (e.g., 'Store 1 Main Display')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier for this screen (used in /signage/play/<slug>/)"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Only active screens can be played"
    )

    layout_type = models.CharField(
        max_length=50,
        choices=LAYOUT_CHOICES,
        default='test',
        help_text="Screen layout template to use"
    )

    # Override fields for custom layouts (Phase 2+)
    html_override = models.TextField(
        blank=True,
        help_text="Custom HTML content (for advanced use)"
    )

    css_override = models.TextField(
        blank=True,
        help_text="Custom CSS styles (for advanced use)"
    )

    js_override = models.TextField(
        blank=True,
        help_text="Custom JavaScript code (for advanced use)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Screen"
        verbose_name_plural = "Screens"
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    def save(self, *args, **kwargs):
        """
        Auto-generate slug from name if not provided.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_play_url(self):
        """
        Get the full play URL for this screen.

        Returns:
            str: Relative URL path (e.g., '/signage/play/test/')
        """
        from django.urls import reverse
        return reverse('digital_signage:screen_play', kwargs={'slug': self.slug})


class SalesData(models.Model):
    """
    Sales data for a specific store and employee on a given date.

    This model stores daily sales totals and is used to display
    real-time sales performance on digital signage displays.
    """

    store = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Store name or identifier"
    )
    employee = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Employee name or identifier"
    )
    total_sales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Total sales amount in dollars"
    )
    date = models.DateField(
        db_index=True,
        help_text="Date of the sales data"
    )

    # Timestamps for tracking when records are created/modified
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sales Data"
        verbose_name_plural = "Sales Data"
        ordering = ['-date', 'store', 'employee']
        # Prevent duplicate entries for the same store/employee/date combination
        unique_together = ['store', 'employee', 'date']
        indexes = [
            models.Index(fields=['-date', 'store']),
            models.Index(fields=['store', 'date']),
        ]

    def __str__(self):
        return f"{self.store} - {self.employee} - {self.date}: ${self.total_sales}"


class KPI(models.Model):
    """
    Key Performance Indicator tracking for stores and employees.

    This model compares sales targets against actual sales performance,
    providing metrics for digital signage displays.
    """

    store = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Store name or identifier"
    )
    employee = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Employee name or identifier"
    )
    sales_target = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Target sales amount in dollars"
    )
    actual_sales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        help_text="Actual sales amount in dollars"
    )
    date = models.DateField(
        db_index=True,
        help_text="Date of the KPI measurement"
    )

    # Timestamps for tracking when records are created/modified
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "KPI"
        verbose_name_plural = "KPIs"
        ordering = ['-date', 'store', 'employee']
        # Prevent duplicate entries for the same store/employee/date combination
        unique_together = ['store', 'employee', 'date']
        indexes = [
            models.Index(fields=['-date', 'store']),
            models.Index(fields=['store', 'date']),
        ]

    def __str__(self):
        return f"{self.store} - {self.employee} - {self.date}: ${self.actual_sales}/${self.sales_target}"

    @property
    def performance_percentage(self):
        """
        Calculate the performance percentage (actual vs target).

        Returns:
            Decimal: Performance as a percentage (e.g., 95.5 for 95.5%)
        """
        if self.sales_target == 0:
            return Decimal('0.00')
        return (self.actual_sales / self.sales_target) * 100

    @property
    def is_on_target(self):
        """
        Check if actual sales meet or exceed the target.

        Returns:
            bool: True if on or above target, False otherwise
        """
        return self.actual_sales >= self.sales_target

    @property
    def variance(self):
        """
        Calculate the variance between actual sales and target.

        Returns:
            Decimal: Difference between actual and target (positive = over, negative = under)
        """
        return self.actual_sales - self.sales_target


class Playlist(models.Model):
    """
    Playlist Model

    Represents a collection of screens that rotate on a device.
    A playlist contains multiple PlaylistItems, each with a screen,
    order, and duration.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this playlist"
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Descriptive name for this playlist (e.g., 'Store 1 Rotation')"
    )

    slug = models.SlugField(
        max_length=200,
        unique=True,
        db_index=True,
        help_text="URL-safe identifier for this playlist"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether this playlist is actively being used"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """Auto-generate slug from name if not provided."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def device_count(self):
        """Return the number of devices using this playlist."""
        return self.device_set.count()


class PlaylistItem(models.Model):
    """
    Playlist Item Model

    Represents a single item within a playlist, with ordering
    and duration information. Can be either a ScreenDesign or MediaAsset.
    """

    ITEM_TYPE_CHOICES = [
        ('screen', 'Screen Design'),
        ('media', 'Media Asset'),
    ]

    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name='items',
        help_text="Playlist this item belongs to"
    )

    item_type = models.CharField(
        max_length=10,
        choices=ITEM_TYPE_CHOICES,
        default='screen',
        help_text="Type of content (screen design or media)"
    )

    # Either screen OR media_asset will be set, not both
    screen = models.ForeignKey(
        ScreenDesign,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Screen design to display (if item_type is 'screen')"
    )

    media_asset = models.ForeignKey(
        MediaAsset,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="Media asset to display (if item_type is 'media')"
    )

    order = models.PositiveIntegerField(
        default=0,
        help_text="Display order (lower numbers shown first)"
    )

    duration_seconds = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(0)],
        help_text="How long to display this item (in seconds). For videos, set to 0 to use video duration."
    )

    class Meta:
        verbose_name = "Playlist Item"
        verbose_name_plural = "Playlist Items"
        ordering = ['playlist', 'order']
        unique_together = ['playlist', 'order']

    def __str__(self):
        content_name = self.content_name
        return f"{self.playlist.name} - {content_name} (Order: {self.order})"

    @property
    def content_name(self):
        """Return the name of the content (screen or media)."""
        if self.item_type == 'screen' and self.screen:
            return self.screen.name
        elif self.item_type == 'media' and self.media_asset:
            return self.media_asset.name
        return 'Unknown'

    @property
    def content_slug(self):
        """Return the slug of the content."""
        if self.item_type == 'screen' and self.screen:
            return self.screen.slug
        elif self.item_type == 'media' and self.media_asset:
            return self.media_asset.slug
        return None

    @property
    def effective_duration(self):
        """
        Return the effective duration for this item.
        For videos with duration_seconds=0, use the video's actual duration.
        """
        if self.item_type == 'media' and self.media_asset:
            if self.duration_seconds == 0 and self.media_asset.duration_seconds:
                return self.media_asset.duration_seconds
        return self.duration_seconds or 30

    def get_player_url(self):
        """Get the player URL for this item."""
        from django.urls import reverse
        if self.item_type == 'screen' and self.screen:
            return reverse('digital_signage:player', kwargs={'slug': self.screen.slug})
        elif self.item_type == 'media' and self.media_asset:
            return reverse('digital_signage:media_player', kwargs={'slug': self.media_asset.slug})
        return None


class Device(models.Model):
    """
    Device Model

    Represents a physical device (Firestick/TV) that displays
    signage content. Devices register with a code, then can be
    assigned playlists or individual screens.
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for this device"
    )

    name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Human-readable device name (e.g., 'Store 1 Main Display')"
    )

    registration_code = models.CharField(
        max_length=8,
        unique=True,
        null=True,
        blank=True,
        help_text="Short code for device registration (e.g., 'ABC123')"
    )

    registered = models.BooleanField(
        default=False,
        help_text="Whether this device has been registered and configured"
    )

    assigned_playlist = models.ForeignKey(
        Playlist,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Playlist assigned to this device (takes precedence over single screen)"
    )

    assigned_screen = models.ForeignKey(
        ScreenDesign,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Single screen assigned to this device (used if no playlist assigned)"
    )

    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Physical location of this device (e.g., 'Store 12, Front Counter')"
    )

    notes = models.TextField(
        blank=True,
        help_text="Internal notes about this device"
    )

    last_seen = models.DateTimeField(
        auto_now_add=True,
        help_text="Last time this device checked in (updated when device polls for config)"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ['-last_seen']
        indexes = [
            models.Index(fields=['registration_code']),
            models.Index(fields=['registered']),
        ]

    def __str__(self):
        if self.name:
            return f"{self.name} ({self.id})"
        return str(self.id)

    @property
    def is_pending_registration(self):
        """Check if device is waiting to be registered."""
        return not self.registered and self.registration_code is not None

    @property
    def status(self):
        """
        Get device status based on last_seen timestamp.

        Returns:
            str: 'online' if seen within 5 minutes,
                 'recent' if seen within 1 hour,
                 'offline' otherwise
        """
        from django.utils import timezone
        from datetime import timedelta

        now = timezone.now()
        diff = now - self.last_seen

        if diff < timedelta(minutes=5):
            return 'online'
        elif diff < timedelta(hours=1):
            return 'recent'
        else:
            return 'offline'
