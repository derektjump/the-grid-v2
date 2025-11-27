"""
Digital Signage Views

This module provides views for the digital signage design and data management portal.

IMPORTANT: This app is NOT a signage player or live dashboard.
It is an INTERNAL DESIGN + DATA PORTAL where we:
  - Design screen content (HTML/CSS/JS)
  - Preview what screens will look like
  - Manage signage-related data
  - Copy final designs into ScreenCloud Playground

Views:
    TABBED OVERVIEW INTERFACE:
    - OverviewView: Main dashboard with Overview/Designs/Playlists/Devices tabs
    - DeviceDetailView: Individual device management page
    - DeviceDeleteView: Delete a device with confirmation

    DESIGN MANAGEMENT VIEWS:
    - ScreenDesignListView: List all screen designs
    - ScreenDesignUpdateView: Create/edit screen designs
    - ScreenDesignPreviewView: Preview a screen design

    PLAYLIST MANAGEMENT VIEWS:
    - PlaylistCreateView: Create new playlists
    - PlaylistUpdateView: Edit existing playlists

    AJAX ENDPOINTS:
    - register_device_with_code: Register a device using its code
    - assign_device_content: Assign playlist or screen to a device

    API ENDPOINTS FOR FIRE TV DEVICES:
    - device_request_code: Request registration code
    - device_register: Mark device as registered
    - device_config: Get device configuration
    - device_config_by_code: Get config by registration code
    - screen_player: Public player for Fire TV devices

    DEPRECATED DASHBOARD VIEWS (kept for backward compatibility):
    - ScreenPlayView: Legacy full-screen player (DEPRECATED)
    - SalesDataListView: Display sales data (DEPRECATED - no longer primary feature)
    - KPIListView: Display KPI metrics (DEPRECATED - no longer primary feature)
    - DisplayDashboardView: Combined dashboard (DEPRECATED - no longer primary feature)
"""

from django.views.generic import ListView, UpdateView, CreateView, DeleteView, TemplateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Avg, Q, F
from django.utils import timezone
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.utils.text import slugify
from datetime import timedelta
from .models import (
    ScreenDesign, Screen, SalesData, KPI, Device, Playlist, PlaylistItem,
    MediaFolder, MediaAsset, generate_registration_code
)
import json
import os


# ============================================================================
# MAIN TABBED OVERVIEW INTERFACE
# ============================================================================

class OverviewView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard with tabbed interface.

    Provides four tabs:
    - Overview: Statistics and quick actions
    - Designs: All screen designs
    - Playlists: All playlists with their screens
    - Devices: All devices with status indicators

    This is the default landing page for Digital Signage.
    """

    template_name = 'digital_signage/overview.html'

    def get_context_data(self, **kwargs):
        """
        Gather all data needed for the tabbed interface.

        Returns:
            dict: Complete context with stats, devices, designs, and playlists
        """
        context = super().get_context_data(**kwargs)

        # Get only registered devices and calculate status counts
        devices = Device.objects.filter(registered=True)
        online_count = sum(1 for d in devices if d.status == 'online')
        recent_count = sum(1 for d in devices if d.status == 'recent')
        offline_count = sum(1 for d in devices if d.status == 'offline')

        # Statistics for Overview tab
        context['stats'] = {
            'total_designs': ScreenDesign.objects.filter(is_active=True).count(),
            'devices_online': online_count,
            'devices_recent': recent_count,
            'devices_offline': offline_count,
            'total_playlists': Playlist.objects.filter(is_active=True).count(),
        }

        # Data for each tab (only show registered devices)
        context['devices'] = devices.order_by('-last_seen')
        context['designs'] = ScreenDesign.objects.all().order_by('-updated_at')
        context['playlists'] = Playlist.objects.all().prefetch_related('items__screen').order_by('name')

        # Media Library data
        context['media_folders'] = MediaFolder.objects.all().order_by('name')
        context['media_assets'] = MediaAsset.objects.filter(is_active=True).select_related('folder').order_by('-created_at')
        context['media_stats'] = {
            'total': MediaAsset.objects.filter(is_active=True).count(),
            'images': MediaAsset.objects.filter(is_active=True, asset_type='image').count(),
            'videos': MediaAsset.objects.filter(is_active=True, asset_type='video').count(),
        }

        return context


class DeviceDetailView(LoginRequiredMixin, UpdateView):
    """
    Individual device management page.

    Allows editing device properties:
    - Name
    - Location
    - Assigned playlist
    - Assigned screen
    - Notes

    Shows device information:
    - ID
    - Registration code
    - Status (online/recent/offline)
    - Timestamps
    """

    model = Device
    template_name = 'digital_signage/device_detail.html'
    fields = ['name', 'location', 'assigned_playlist', 'assigned_screen', 'notes']
    success_url = reverse_lazy('digital_signage:overview')

    def get_context_data(self, **kwargs):
        """
        Add device status and available content to context.

        Returns:
            dict: Context with device info, status, playlists, and designs
        """
        context = super().get_context_data(**kwargs)
        context['device_status'] = self.object.status
        context['available_playlists'] = Playlist.objects.filter(is_active=True)
        context['available_designs'] = ScreenDesign.objects.filter(is_active=True)
        return context


class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a device with confirmation.

    Provides a confirmation page before deletion.
    Redirects to overview after successful deletion.
    """

    model = Device
    template_name = 'digital_signage/device_confirm_delete.html'
    success_url = reverse_lazy('digital_signage:overview')


class ScreenDesignDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a screen design with confirmation.

    Checks if the design is used by any devices or playlists before deletion.
    Redirects to overview after successful deletion.
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_confirm_delete.html'
    success_url = reverse_lazy('digital_signage:overview')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        design = self.get_object()
        # Check if used by devices
        context['device_count'] = Device.objects.filter(assigned_screen=design).count()
        # Check if used in playlists
        context['playlist_count'] = PlaylistItem.objects.filter(screen=design).count()
        return context


class PlaylistDeleteView(LoginRequiredMixin, DeleteView):
    """
    Delete a playlist with confirmation.

    Checks if the playlist is assigned to any devices before deletion.
    Redirects to overview after successful deletion.
    """

    model = Playlist
    template_name = 'digital_signage/playlist_confirm_delete.html'
    success_url = reverse_lazy('digital_signage:overview')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        playlist = self.get_object()
        # Check if used by devices
        context['device_count'] = Device.objects.filter(assigned_playlist=playlist).count()
        return context


# ============================================================================
# AJAX ENDPOINTS FOR UI INTERACTIONS
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def register_device_with_code(request):
    """
    AJAX endpoint to register a device using its registration code.

    This is called from the "Add Device" modal when a user enters
    a registration code displayed on a Fire TV device.

    Request Body (JSON):
        {
            "code": "ABC123"
        }

    Returns:
        JSON: {
            "success": true,
            "device": {
                "id": "uuid",
                "name": "Device name",
                "registration_code": "ABC123"
            }
        }
        OR
        JSON: {
            "success": false,
            "error": "Error message"
        }

    HTTP Status Codes:
        200: Success - device registered
        400: Bad Request - invalid JSON or missing code
        404: Device not found with that code
        500: Server error
    """
    try:
        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Get registration code
        code = data.get('code', '').strip().upper()
        if not code:
            return JsonResponse({
                'success': False,
                'error': 'Registration code is required'
            }, status=400)

        # Find device by registration code
        try:
            device = Device.objects.get(registration_code=code)
        except Device.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': f'No device found with registration code: {code}'
            }, status=404)

        # Mark device as registered
        device.registered = True

        # Auto-assign welcome screen if no content assigned
        if not device.assigned_playlist and not device.assigned_screen:
            try:
                welcome_screen = ScreenDesign.objects.get(slug='welcome-screen')
                device.assigned_screen = welcome_screen
            except ScreenDesign.DoesNotExist:
                pass  # Welcome screen doesn't exist yet, skip auto-assignment

        device.save()

        # Return success with device info
        return JsonResponse({
            'success': True,
            'device': {
                'id': str(device.id),
                'name': device.name or f'Device {code}',
                'registration_code': device.registration_code,
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def assign_device_content(request, pk):
    """
    AJAX endpoint to assign content (playlist or screen) to a device.

    Called when clicking "Assign Playlist" or "Assign Screen" buttons
    on device cards in the overview.

    URL Parameters:
        pk: Device UUID

    Request Body (JSON):
        {
            "playlist_id": "uuid"  // OR
            "screen_id": "uuid"
        }

    Returns:
        JSON: {
            "success": true,
            "device_id": "uuid",
            "assigned_type": "playlist" | "screen",
            "assigned_name": "Content name"
        }
        OR
        JSON: {
            "success": false,
            "error": "Error message"
        }

    HTTP Status Codes:
        200: Success - content assigned
        400: Bad Request - invalid JSON or missing data
        404: Device, playlist, or screen not found
        500: Server error
    """
    try:
        # Get device
        try:
            device = Device.objects.get(id=pk)
        except Device.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Device not found'
            }, status=404)

        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Check what type of content to assign
        playlist_id = data.get('playlist_id')
        screen_id = data.get('screen_id')

        if not playlist_id and not screen_id:
            return JsonResponse({
                'success': False,
                'error': 'Either playlist_id or screen_id is required'
            }, status=400)

        # Assign playlist
        if playlist_id:
            try:
                playlist = Playlist.objects.get(id=playlist_id)
                device.assigned_playlist = playlist
                device.assigned_screen = None  # Clear screen assignment
                device.save()

                return JsonResponse({
                    'success': True,
                    'device_id': str(device.id),
                    'assigned_type': 'playlist',
                    'assigned_name': playlist.name
                })
            except Playlist.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Playlist not found'
                }, status=404)

        # Assign screen
        if screen_id:
            try:
                screen = ScreenDesign.objects.get(id=screen_id)
                device.assigned_screen = screen
                device.assigned_playlist = None  # Clear playlist assignment
                device.save()

                return JsonResponse({
                    'success': True,
                    'device_id': str(device.id),
                    'assigned_type': 'screen',
                    'assigned_name': screen.name
                })
            except ScreenDesign.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Screen design not found'
                }, status=404)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


# ============================================================================
# MEDIA LIBRARY AJAX ENDPOINTS
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def upload_media(request):
    """
    AJAX endpoint to upload media files (images/videos).

    Handles multipart form data with multiple files.
    Creates MediaAsset records for each uploaded file.

    Request:
        multipart/form-data with:
        - files: One or more file uploads
        - folder: Optional folder UUID to place files in

    Returns:
        JSON: {
            "success": true,
            "uploaded_count": 3,
            "assets": [
                {"id": "uuid", "name": "file.jpg", "type": "image"},
                ...
            ]
        }

    HTTP Status Codes:
        200: Success - files uploaded
        400: Bad Request - no files or invalid data
        500: Server error
    """
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        # Get uploaded files
        files = request.FILES.getlist('files')
        if not files:
            return JsonResponse({
                'success': False,
                'error': 'No files provided'
            }, status=400)

        # Get optional folder
        folder = None
        folder_id = request.POST.get('folder')
        if folder_id:
            try:
                folder = MediaFolder.objects.get(id=folder_id)
            except MediaFolder.DoesNotExist:
                pass  # Folder not found, use uncategorized

        # Process each file
        uploaded_assets = []
        allowed_image_ext = ['jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp']
        allowed_video_ext = ['mp4', 'webm', 'mov', 'avi']
        max_size = 100 * 1024 * 1024  # 100MB

        for file in files:
            # Check file size
            if file.size > max_size:
                continue  # Skip oversized files

            # Determine file type from extension
            file_ext = file.name.rsplit('.', 1)[-1].lower() if '.' in file.name else ''

            if file_ext in allowed_image_ext:
                asset_type = 'image'
            elif file_ext in allowed_video_ext:
                asset_type = 'video'
            else:
                continue  # Skip unsupported files

            # Generate unique slug
            base_name = os.path.splitext(file.name)[0]
            slug = slugify(base_name)
            if not slug:
                slug = 'media'

            # Ensure slug is unique
            original_slug = slug
            counter = 1
            while MediaAsset.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1

            # Create asset
            asset = MediaAsset.objects.create(
                name=base_name,
                slug=slug,
                file=file,
                asset_type=asset_type,
                folder=folder,
                file_size=file.size
            )

            uploaded_assets.append({
                'id': str(asset.id),
                'name': asset.name,
                'type': asset_type
            })

        if not uploaded_assets:
            return JsonResponse({
                'success': False,
                'error': 'No valid files to upload'
            }, status=400)

        return JsonResponse({
            'success': True,
            'uploaded_count': len(uploaded_assets),
            'assets': uploaded_assets
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def create_folder(request):
    """
    AJAX endpoint to create a media folder.

    Request Body (JSON):
        {
            "name": "Folder Name",
            "description": "Optional description"
        }

    Returns:
        JSON: {
            "success": true,
            "folder": {
                "id": "uuid",
                "name": "Folder Name",
                "slug": "folder-name"
            }
        }

    HTTP Status Codes:
        200: Success - folder created
        400: Bad Request - invalid data or duplicate slug
        500: Server error
    """
    try:
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Get folder name
        name = data.get('name', '').strip()
        if not name:
            return JsonResponse({
                'success': False,
                'error': 'Folder name is required'
            }, status=400)

        # Generate slug
        slug = slugify(name)
        if not slug:
            slug = 'folder'

        # Ensure slug is unique
        original_slug = slug
        counter = 1
        while MediaFolder.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        # Create folder
        folder = MediaFolder.objects.create(
            name=name,
            slug=slug,
            description=data.get('description', '').strip()
        )

        return JsonResponse({
            'success': True,
            'folder': {
                'id': str(folder.id),
                'name': folder.name,
                'slug': folder.slug
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_media(request, media_id):
    """
    AJAX endpoint to get media asset details.

    URL Parameters:
        media_id: UUID of the media asset

    Returns:
        JSON: {
            "success": true,
            "asset": {
                "id": "uuid",
                "name": "Asset Name",
                "slug": "asset-slug",
                "asset_type": "image|video",
                "file_url": "/media/...",
                "file_size": 1234567,
                "file_size_display": "1.2 MB",
                "folder_id": "uuid" or null,
                "folder_name": "Folder Name" or null,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        asset = get_object_or_404(MediaAsset, id=media_id)

        return JsonResponse({
            'success': True,
            'asset': {
                'id': str(asset.id),
                'name': asset.name,
                'slug': asset.slug,
                'asset_type': asset.asset_type,
                'file_url': asset.file.url,
                'file_size': asset.file_size,
                'file_size_display': asset.file_size_display,
                'folder_id': str(asset.folder.id) if asset.folder else None,
                'folder_name': asset.folder.name if asset.folder else None,
                'created_at': asset.created_at.isoformat()
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def update_media(request, media_id):
    """
    AJAX endpoint to update a media asset (name, folder).

    URL Parameters:
        media_id: UUID of the media asset

    Request Body (JSON):
        {
            "name": "New Name" (optional),
            "folder_id": "uuid" or null (optional - null removes from folder)
        }

    Returns:
        JSON: {
            "success": true,
            "asset": { ... }
        }
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        asset = get_object_or_404(MediaAsset, id=media_id)

        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Update name if provided
        if 'name' in data:
            name = data['name'].strip()
            if name:
                asset.name = name

        # Update folder if provided
        if 'folder_id' in data:
            folder_id = data['folder_id']
            if folder_id:
                try:
                    asset.folder = MediaFolder.objects.get(id=folder_id)
                except MediaFolder.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'error': 'Folder not found'
                    }, status=404)
            else:
                asset.folder = None

        asset.save()

        return JsonResponse({
            'success': True,
            'asset': {
                'id': str(asset.id),
                'name': asset.name,
                'folder_id': str(asset.folder.id) if asset.folder else None,
                'folder_name': asset.folder.name if asset.folder else None,
                'folder_slug': asset.folder.slug if asset.folder else None
            }
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE", "POST"])
def delete_media(request, media_id):
    """
    AJAX endpoint to delete a media asset.

    URL Parameters:
        media_id: UUID of the media asset

    Returns:
        JSON: {
            "success": true,
            "message": "Media deleted successfully"
        }

    HTTP Status Codes:
        200: Success - media deleted
        401: Authentication required
        404: Media asset not found
        500: Server error
    """
    try:
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'error': 'Authentication required'
            }, status=401)

        asset = get_object_or_404(MediaAsset, id=media_id)

        # Check if media is used in any playlists
        playlist_count = PlaylistItem.objects.filter(media_asset=asset).count()
        if playlist_count > 0:
            return JsonResponse({
                'success': False,
                'error': f'Cannot delete: media is used in {playlist_count} playlist(s). Remove it from playlists first.'
            }, status=400)

        # Delete the file from storage
        if asset.file:
            asset.file.delete(save=False)

        # Delete the asset record
        asset_name = asset.name
        asset.delete()

        return JsonResponse({
            'success': True,
            'message': f'Media "{asset_name}" deleted successfully'
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Server error: {str(e)}'
        }, status=500)


# ============================================================================
# PLAYLIST MANAGEMENT VIEWS
# ============================================================================

class PlaylistCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new playlist.

    Allows creating a playlist with multiple screens and media assets,
    each with custom duration and ordering.

    Uses formsets to handle multiple PlaylistItem entries.
    """

    model = Playlist
    template_name = 'digital_signage/playlist_form.html'
    fields = ['name', 'slug', 'is_active']
    success_url = reverse_lazy('digital_signage:overview')

    def get_context_data(self, **kwargs):
        """
        Add available screens, media, and mode indicator to context.

        Returns:
            dict: Context with available screens, media, and is_create_mode flag
        """
        context = super().get_context_data(**kwargs)
        context['available_screens'] = ScreenDesign.objects.filter(is_active=True).order_by('name')
        context['available_media'] = MediaAsset.objects.filter(is_active=True).order_by('name')
        context['is_create_mode'] = True
        return context

    def form_valid(self, form):
        """
        Handle form submission and create playlist items.

        Processes the hidden inputs created by JavaScript:
        - new_type_N: Item type ('screen' or 'media')
        - new_item_N: Item ID (screen or media UUID)
        - new_duration_N: Duration for that item

        Returns:
            HttpResponse: Redirect to success URL
        """
        response = super().form_valid(form)

        # Process new playlist items from POST data
        order = 0
        processed_nums = set()

        for key in self.request.POST:
            if key.startswith('new_item_'):
                item_num = key.replace('new_item_', '')
                if item_num in processed_nums:
                    continue
                processed_nums.add(item_num)

                item_id = self.request.POST.get(key)
                item_type = self.request.POST.get(f'new_type_{item_num}', 'screen')
                duration = int(self.request.POST.get(f'new_duration_{item_num}', 30))

                if item_id:
                    try:
                        if item_type == 'media':
                            media = MediaAsset.objects.get(id=item_id)
                            PlaylistItem.objects.create(
                                playlist=self.object,
                                item_type='media',
                                media_asset=media,
                                order=order,
                                duration_seconds=duration
                            )
                        else:
                            screen = ScreenDesign.objects.get(id=item_id)
                            PlaylistItem.objects.create(
                                playlist=self.object,
                                item_type='screen',
                                screen=screen,
                                order=order,
                                duration_seconds=duration
                            )
                        order += 1
                    except (ScreenDesign.DoesNotExist, MediaAsset.DoesNotExist):
                        pass

        return response


class PlaylistUpdateView(LoginRequiredMixin, UpdateView):
    """
    Edit an existing playlist.

    Allows updating playlist metadata and reordering/modifying
    the screens and media within the playlist.

    Uses formsets to handle multiple PlaylistItem entries.
    """

    model = Playlist
    template_name = 'digital_signage/playlist_form.html'
    fields = ['name', 'slug', 'is_active']
    success_url = reverse_lazy('digital_signage:overview')

    def get_context_data(self, **kwargs):
        """
        Add playlist items, available screens, and media to context.

        Returns:
            dict: Context with playlist items, available screens, media, and is_create_mode flag
        """
        context = super().get_context_data(**kwargs)
        context['playlist_items'] = self.object.items.select_related('screen', 'media_asset').order_by('order')
        context['available_screens'] = ScreenDesign.objects.filter(is_active=True).order_by('name')
        context['available_media'] = MediaAsset.objects.filter(is_active=True).order_by('name')
        context['is_create_mode'] = False
        return context

    def form_valid(self, form):
        """
        Handle form submission and update playlist items.

        Processes:
        - new_type_N: Item type ('screen' or 'media')
        - new_item_N: Item ID (screen or media UUID)
        - new_duration_N: Duration for that item

        Returns:
            HttpResponse: Redirect to success URL
        """
        response = super().form_valid(form)

        # Clear existing items and recreate from form data
        # This ensures proper ordering based on the DOM order
        self.object.items.all().delete()

        order = 0
        processed_nums = set()

        # Process new playlist items from POST data
        for key in sorted(self.request.POST.keys()):
            if key.startswith('new_item_'):
                item_num = key.replace('new_item_', '')
                if item_num in processed_nums:
                    continue
                processed_nums.add(item_num)

                item_id = self.request.POST.get(key)
                item_type = self.request.POST.get(f'new_type_{item_num}', 'screen')
                duration = int(self.request.POST.get(f'new_duration_{item_num}', 30))

                if item_id:
                    try:
                        if item_type == 'media':
                            media = MediaAsset.objects.get(id=item_id)
                            PlaylistItem.objects.create(
                                playlist=self.object,
                                item_type='media',
                                media_asset=media,
                                order=order,
                                duration_seconds=duration
                            )
                        else:
                            screen = ScreenDesign.objects.get(id=item_id)
                            PlaylistItem.objects.create(
                                playlist=self.object,
                                item_type='screen',
                                screen=screen,
                                order=order,
                                duration_seconds=duration
                            )
                        order += 1
                    except (ScreenDesign.DoesNotExist, MediaAsset.DoesNotExist):
                        pass

        return response


# ============================================================================
# API ENDPOINTS FOR SCREENCLOUD / EXTERNAL INTEGRATIONS
# ============================================================================

@csrf_exempt  # CSRF exemption required for external API calls
@require_http_methods(["GET"])  # Only allow GET requests
def test_profit_data(request):
    """
    API endpoint for ScreenCloud to fetch test profit data by location.

    This endpoint returns static test data to verify ScreenCloud connectivity.
    In the future, this will be replaced with live data from the database.

    Authentication:
        Requires API key via header (X-API-KEY) or query parameter (api_key)

    Returns:
        JSON: {
            "items": [
                {"store": "Store Name", "profit": 123456, "devices": 42},
                ...
            ]
        }

    HTTP Status Codes:
        200: Success - returns test data
        403: Forbidden - invalid or missing API key

    Example Usage:
        fetch("https://app.azurewebsites.net/signage/api/test-profit-by-location/", {
            headers: { "X-API-KEY": "your-api-key-here" }
        })

    CORS Note:
        CORS headers will need to be configured once ScreenCloud's exact origin is known.
        For now, this endpoint is accessible but requires API key authentication.
    """
    # Extract API key from header or query parameter
    api_key = request.headers.get('X-API-KEY') or request.GET.get('api_key')

    # Validate API key against environment variable
    expected_key = getattr(settings, 'SIGNAGE_API_KEY', '')

    if not expected_key:
        # API key not configured in environment
        return HttpResponseForbidden("API authentication is not configured on the server.")

    if not api_key or api_key != expected_key:
        # API key missing or incorrect
        return HttpResponseForbidden("Invalid or missing API key.")

    # Static test data for ScreenCloud connectivity testing
    # TODO: Replace with live database queries once connectivity is verified
    test_data = {
        "items": [
            {"store": "Regina Downtown", "profit": 123456, "devices": 42},
            {"store": "Regina East", "profit": 98765, "devices": 35},
            {"store": "Moose Jaw", "profit": 45678, "devices": 18},
        ]
    }

    return JsonResponse(test_data)


# ============================================================================
# DEVICE MANAGEMENT API ENDPOINTS
# ============================================================================

@csrf_exempt
@require_http_methods(["POST"])
def device_request_code(request):
    """
    API endpoint for Fire TV app to request a registration code.

    This creates a new Device record with a unique registration code
    that the user can enter in the admin to assign content.

    Authentication: None (public endpoint for device registration)

    Request Body (JSON):
        {
            "device_name": "Optional friendly name"
        }

    Returns:
        JSON: {
            "success": true,
            "device_id": "uuid",
            "registration_code": "ABC123"
        }

    HTTP Status Codes:
        200: Success - returns device ID and registration code
        400: Bad Request - invalid JSON
        500: Server error
    """
    try:
        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Generate unique registration code
        code = generate_registration_code()

        # Ensure code is unique
        while Device.objects.filter(registration_code=code).exists():
            code = generate_registration_code()

        # Create device with registration code
        device = Device.objects.create(
            name=data.get('device_name', ''),
            registration_code=code,
            registered=False
        )

        return JsonResponse({
            'success': True,
            'device_id': str(device.id),
            'registration_code': code
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def device_register(request, device_id):
    """
    API endpoint for Fire TV app to mark device as registered.

    Called after the user has entered the registration code in the admin
    and assigned content to the device.

    Authentication: None (uses device UUID for identification)

    URL Parameters:
        device_id: UUID of the device

    Request Body (JSON):
        {
            "registration_code": "ABC123"
        }

    Returns:
        JSON: {
            "success": true,
            "registered": true
        }

    HTTP Status Codes:
        200: Success - device registered
        400: Bad Request - invalid code or JSON
        404: Device not found
        500: Server error
    """
    try:
        # Get device
        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Device not found'
            }, status=404)

        # Parse request body
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid JSON in request body'
            }, status=400)

        # Verify registration code
        provided_code = data.get('registration_code', '')
        if provided_code != device.registration_code:
            return JsonResponse({
                'success': False,
                'error': 'Invalid registration code'
            }, status=400)

        # Mark device as registered
        device.registered = True
        device.save()

        return JsonResponse({
            'success': True,
            'registered': True
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def device_config(request, device_id):
    """
    API endpoint for Fire TV app to fetch device configuration.

    Returns the assigned playlist or screen for the device.

    Authentication: None (uses device UUID for identification)

    URL Parameters:
        device_id: UUID of the device

    Returns:
        JSON: {
            "success": true,
            "device_id": "uuid",
            "device_name": "Store 1 Main Display",
            "registered": true,
            "config": {
                "type": "playlist" | "screen" | "none",
                "playlist_id": "uuid" (if type=playlist),
                "playlist_name": "Store Rotation" (if type=playlist),
                "items": [  (if type=playlist)
                    {
                        "screen_id": "uuid",
                        "screen_name": "Sales Dashboard",
                        "screen_slug": "sales-dashboard",
                        "player_url": "https://domain/player/sales-dashboard/",
                        "duration_seconds": 30,
                        "order": 0
                    }
                ],
                "screen_id": "uuid" (if type=screen),
                "screen_name": "Sales Dashboard" (if type=screen),
                "screen_slug": "sales-dashboard" (if type=screen),
                "player_url": "https://domain/player/sales-dashboard/" (if type=screen)
            }
        }

    HTTP Status Codes:
        200: Success - returns device configuration
        404: Device not found
        500: Server error
    """
    try:
        # Get device
        try:
            device = Device.objects.get(id=device_id)
        except Device.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Device not found'
            }, status=404)

        # Update last_seen timestamp to track device connectivity
        from django.utils import timezone
        device.last_seen = timezone.now()
        device.save(update_fields=['last_seen'])

        # Build base URL for player endpoints
        base_url = request.build_absolute_uri('/').rstrip('/')

        # Build configuration based on assigned content
        config = {'type': 'none'}

        if device.assigned_playlist:
            # Playlist assigned - return all items (screens and media) in order
            playlist = device.assigned_playlist
            items = playlist.items.select_related('screen', 'media_asset').order_by('order')

            playlist_items = []
            for item in items:
                if item.item_type == 'media' and item.media_asset:
                    # Media asset item
                    asset = item.media_asset
                    playlist_items.append({
                        'item_type': 'media',
                        'media_id': str(asset.id),
                        'media_name': asset.name,
                        'media_slug': asset.slug,
                        'media_type': asset.asset_type,
                        'player_url': f"{base_url}{reverse('digital_signage:media_player', kwargs={'slug': asset.slug})}",
                        'file_url': f"{base_url}{asset.file.url}",
                        'duration_seconds': item.effective_duration,
                        'order': item.order
                    })
                elif item.screen:
                    # Screen design item
                    playlist_items.append({
                        'item_type': 'screen',
                        'screen_id': str(item.screen.id),
                        'screen_name': item.screen.name,
                        'screen_slug': item.screen.slug,
                        'player_url': f"{base_url}{reverse('digital_signage:screen_player', kwargs={'slug': item.screen.slug})}",
                        'duration_seconds': item.duration_seconds,
                        'order': item.order
                    })

            config = {
                'type': 'playlist',
                'playlist_id': str(playlist.id),
                'playlist_name': playlist.name,
                'items': playlist_items
            }

        elif device.assigned_screen:
            # Single screen assigned
            screen = device.assigned_screen

            config = {
                'type': 'screen',
                'screen_id': str(screen.id),
                'screen_name': screen.name,
                'screen_slug': screen.slug,
                'player_url': f"{base_url}{reverse('digital_signage:screen_player', kwargs={'slug': screen.slug})}"
            }

        return JsonResponse({
            'success': True,
            'device_id': str(device.id),
            'device_name': device.name,
            'registered': device.registered,
            'config': config
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def device_config_by_code(request, code):
    """
    API endpoint for Fire TV app to fetch device configuration by registration code.

    Alternative to device_config endpoint when device only knows its registration code.

    Authentication: None (uses registration code for identification)

    URL Parameters:
        code: Registration code (e.g., "ABC123")

    Returns:
        Same as device_config endpoint

    HTTP Status Codes:
        200: Success - returns device configuration
        404: Device not found with that code
        500: Server error
    """
    try:
        # Get device by registration code
        try:
            device = Device.objects.get(registration_code=code)
        except Device.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Device not found with that registration code'
            }, status=404)

        # Forward to main config endpoint
        return device_config(request, str(device.id))

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


# ============================================================================
# ACTIVE DESIGN MANAGEMENT VIEWS
# ============================================================================

class ScreenDesignListView(LoginRequiredMixin, ListView):
    """
    List view for all screen designs.

    Displays all screen design templates with their metadata,
    allowing users to browse, edit, and preview designs.

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_list.html'
    context_object_name = 'designs'
    paginate_by = 20

    def get_queryset(self):
        """
        Get queryset with optional filtering.

        Returns:
            QuerySet: Filtered screen designs
        """
        queryset = super().get_queryset()

        # Filter by active status if requested
        status = self.request.GET.get('status')
        if status == 'active':
            queryset = queryset.filter(is_active=True)
        elif status == 'inactive':
            queryset = queryset.filter(is_active=False)

        # Search by name or slug
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(slug__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['total_designs'] = ScreenDesign.objects.count()
        context['active_designs'] = ScreenDesign.objects.filter(is_active=True).count()
        return context


class ScreenDesignUpdateView(LoginRequiredMixin, UpdateView):
    """
    Create/Edit view for screen designs.

    Allows users to create new screen designs or edit existing ones.
    Provides large text areas for HTML/CSS/JS code editing.

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_form.html'
    fields = ['name', 'slug', 'description', 'html_code', 'css_code', 'js_code', 'notes', 'is_active']
    success_url = reverse_lazy('digital_signage:overview')

    def get_object(self, queryset=None):
        """
        Get the object to edit, or None for create mode.

        Returns:
            ScreenDesign or None: The design to edit, or None for new
        """
        slug = self.kwargs.get('slug')
        if slug:
            return get_object_or_404(ScreenDesign, slug=slug)
        return None

    def get_context_data(self, **kwargs):
        """
        Add mode indicator to context.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)
        context['is_create_mode'] = self.object is None
        return context

    def get(self, request, *args, **kwargs):
        """
        Handle GET request for create or edit.

        Returns:
            HttpResponse: Rendered form
        """
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request for create or edit.

        Returns:
            HttpResponse: Redirect or form with errors
        """
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)


class ScreenDesignPreviewView(LoginRequiredMixin, DetailView):
    """
    Preview view for screen designs.

    Renders a barebones HTML shell that displays the screen design
    exactly as it would appear on a TV screen. This is for internal
    preview only - the actual playback happens in ScreenCloud.

    The view injects:
    - CSS code into a <style> block
    - HTML code into the body
    - JavaScript code into a <script> block

    Access: Staff/authenticated users only
    """

    model = ScreenDesign
    template_name = 'digital_signage/screen_design_preview.html'
    context_object_name = 'screen_design'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        """
        Get queryset (no filtering needed for preview).

        Returns:
            QuerySet: All screen designs
        """
        return ScreenDesign.objects.all()


@require_http_methods(["GET"])
def screen_player(request, slug):
    """
    Public full-screen player view for Fire TV devices.

    This view renders a screen design in full-screen mode without
    authentication, navigation, or any UI chrome. It is designed
    to be loaded in a WebView on Fire TV devices.

    Unlike ScreenDesignPreviewView (which requires login), this is
    a public endpoint intended for device playback.

    URL Parameters:
        slug: Screen design slug

    Returns:
        Rendered player template with screen design code injected

    HTTP Status Codes:
        200: Success - renders player
        404: Screen design not found or inactive
    """
    # Get active screen design
    screen_design = get_object_or_404(ScreenDesign, slug=slug, is_active=True)

    # Render barebones player template
    return render(request, 'digital_signage/player.html', {
        'screen_design': screen_design
    })


@require_http_methods(["GET"])
def media_player(request, slug):
    """
    Public full-screen player view for media assets on Fire TV devices.

    This view renders a media asset (image or video) in full-screen mode
    without authentication, navigation, or any UI chrome. It is designed
    to be loaded in a WebView on Fire TV devices.

    URL Parameters:
        slug: Media asset slug

    Returns:
        Rendered media player template

    HTTP Status Codes:
        200: Success - renders media player
        404: Media asset not found or inactive
    """
    # Get active media asset
    media_asset = get_object_or_404(MediaAsset, slug=slug, is_active=True)

    # Render media player template
    return render(request, 'digital_signage/media_player.html', {
        'media_asset': media_asset
    })


# ============================================================================
# DEPRECATED VIEWS (kept for backward compatibility)
# ============================================================================
# These views were created when digital_signage was a sales dashboard.
# They are DEPRECATED and should not be used for new features.
# They will be removed or repurposed in a future version.
# ============================================================================

class ScreenPlayView(TemplateView):
    """
    DEPRECATED: Legacy full-screen player view for ScreenCloud integration.

    This view was designed for anonymous playback of screen content.
    It is no longer the primary feature of this app.

    Use ScreenDesign and ScreenDesignPreviewView instead.
    """

    def get_template_names(self):
        """
        Dynamically select template based on screen layout type.

        Returns:
            list: Template names to try
        """
        screen = self.get_screen()
        layout_type = screen.layout_type

        # Map layout types to templates
        template_map = {
            'test': 'digital_signage/screen_test_play.html',
        }

        return [template_map.get(layout_type, 'digital_signage/screen_test_play.html')]

    def get_screen(self):
        """
        Get the Screen object from the URL slug.

        Returns:
            Screen: The screen instance

        Raises:
            Http404: If screen not found or not active
        """
        slug = self.kwargs.get('slug')
        screen = get_object_or_404(Screen, slug=slug, is_active=True)
        return screen

    def get_context_data(self, **kwargs):
        """
        Add screen data and test data to context.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        screen = self.get_screen()
        context['screen'] = screen

        # Layout-specific context
        if screen.layout_type == 'test':
            # Provide placeholder test data for the test layout
            context['test_data'] = [
                {
                    'store_name': 'Downtown Store',
                    'profit': 123456.78,
                    'device_sales': 42,
                },
                {
                    'store_name': 'West End Location',
                    'profit': 89012.34,
                    'device_sales': 28,
                },
                {
                    'store_name': 'North Branch',
                    'profit': 156789.01,
                    'device_sales': 55,
                },
            ]

        return context


class SalesDataListView(LoginRequiredMixin, ListView):
    """
    DEPRECATED: List view for displaying sales data.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    model = SalesData
    template_name = 'digital_signage/sales_data_list.html'
    context_object_name = 'sales_data'
    paginate_by = 50

    def get_queryset(self):
        """
        Filter queryset based on query parameters.

        Returns:
            QuerySet: Filtered sales data
        """
        queryset = super().get_queryset()

        # Filter by store if provided
        store = self.request.GET.get('store')
        if store:
            queryset = queryset.filter(store__icontains=store)

        # Filter by date range (default: last 7 days)
        days = int(self.request.GET.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        queryset = queryset.filter(date__gte=start_date)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        # Add filter parameters to context
        context['selected_store'] = self.request.GET.get('store', '')
        context['selected_days'] = int(self.request.GET.get('days', 7))

        # Add summary statistics
        queryset = self.get_queryset()
        context['total_sales'] = queryset.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
        context['average_sales'] = queryset.aggregate(Avg('total_sales'))['total_sales__avg'] or 0

        # Get unique stores for filter dropdown
        context['available_stores'] = SalesData.objects.values_list('store', flat=True).distinct().order_by('store')

        return context


class KPIListView(LoginRequiredMixin, ListView):
    """
    DEPRECATED: List view for displaying KPI metrics.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    model = KPI
    template_name = 'digital_signage/kpi_list.html'
    context_object_name = 'kpi_data'
    paginate_by = 50

    def get_queryset(self):
        """
        Filter queryset based on query parameters.

        Returns:
            QuerySet: Filtered KPI data
        """
        queryset = super().get_queryset()

        # Filter by store if provided
        store = self.request.GET.get('store')
        if store:
            queryset = queryset.filter(store__icontains=store)

        # Filter by date range (default: last 7 days)
        days = int(self.request.GET.get('days', 7))
        start_date = timezone.now().date() - timedelta(days=days)
        queryset = queryset.filter(date__gte=start_date)

        # Filter by performance status if provided
        status = self.request.GET.get('status')
        if status == 'on_target':
            queryset = queryset.filter(actual_sales__gte=F('sales_target'))
        elif status == 'under_target':
            queryset = queryset.filter(actual_sales__lt=F('sales_target'))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add additional context for the template.

        Returns:
            dict: Template context
        """
        context = super().get_context_data(**kwargs)

        # Add filter parameters to context
        context['selected_store'] = self.request.GET.get('store', '')
        context['selected_days'] = int(self.request.GET.get('days', 7))
        context['selected_status'] = self.request.GET.get('status', '')

        # Add summary statistics
        queryset = self.get_queryset()
        context['total_target'] = queryset.aggregate(Sum('sales_target'))['sales_target__sum'] or 0
        context['total_actual'] = queryset.aggregate(Sum('actual_sales'))['actual_sales__sum'] or 0

        # Calculate overall performance percentage
        if context['total_target'] > 0:
            context['overall_performance'] = (context['total_actual'] / context['total_target']) * 100
        else:
            context['overall_performance'] = 0

        # Count on-target vs under-target
        context['on_target_count'] = queryset.filter(actual_sales__gte=F('sales_target')).count()
        context['under_target_count'] = queryset.filter(actual_sales__lt=F('sales_target')).count()

        # Get unique stores for filter dropdown
        context['available_stores'] = KPI.objects.values_list('store', flat=True).distinct().order_by('store')

        return context


class DisplayDashboardView(LoginRequiredMixin, TemplateView):
    """
    DEPRECATED: Combined dashboard view for digital signage displays.

    This view was created when digital_signage was a sales dashboard.
    It is no longer the primary feature of this app.
    """

    template_name = 'digital_signage/display_dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Gather all necessary data for the dashboard display.

        Returns:
            dict: Complete dashboard context
        """
        context = super().get_context_data(**kwargs)

        # Get today's date
        today = timezone.now().date()

        # Filter by store if provided in URL
        store_filter = self.request.GET.get('store')

        # Get today's sales data
        sales_queryset = SalesData.objects.filter(date=today)
        if store_filter:
            sales_queryset = sales_queryset.filter(store=store_filter)

        # Get today's KPI data
        kpi_queryset = KPI.objects.filter(date=today)
        if store_filter:
            kpi_queryset = kpi_queryset.filter(store=store_filter)

        # Add to context
        context['todays_sales'] = sales_queryset
        context['todays_kpis'] = kpi_queryset
        context['selected_store'] = store_filter

        # Calculate daily totals
        context['daily_sales_total'] = sales_queryset.aggregate(Sum('total_sales'))['total_sales__sum'] or 0
        context['daily_target_total'] = kpi_queryset.aggregate(Sum('sales_target'))['sales_target__sum'] or 0
        context['daily_actual_total'] = kpi_queryset.aggregate(Sum('actual_sales'))['actual_sales__sum'] or 0

        # Calculate daily performance
        if context['daily_target_total'] > 0:
            context['daily_performance'] = (context['daily_actual_total'] / context['daily_target_total']) * 100
        else:
            context['daily_performance'] = 0

        # Get top performers (top 5 by sales for today)
        context['top_performers'] = sales_queryset.order_by('-total_sales')[:5]

        # Auto-refresh interval (in seconds) for digital signage
        context['refresh_interval'] = 60  # Refresh every 60 seconds

        return context
