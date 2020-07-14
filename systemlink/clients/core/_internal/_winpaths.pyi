# -*- coding: utf-8 -*-

import ctypes
from ctypes import wintypes
from uuid import UUID


class GUID(ctypes.Structure):
    def __init__(self, uuid_: UUID) -> None: ...


class FOLDERID:
    AccountPictures = ...  # type: UUID
    AdminTools = ...  # type: UUID
    ApplicationShortcuts = ...  # type: UUID
    CameraRoll = ...  # type: UUID
    CDBurning = ...  # type: UUID
    CommonAdminTools = ...  # type: UUID
    CommonOEMLinks = ...  # type: UUID
    CommonPrograms = ...  # type: UUID
    CommonStartMenu = ...  # type: UUID
    CommonStartup = ...  # type: UUID
    CommonTemplates = ...  # type: UUID
    Contacts = ...  # type: UUID
    Cookies = ...  # type: UUID
    Desktop = ...  # type: UUID
    DeviceMetadataStore = ...  # type: UUID
    Documents = ...  # type: UUID
    DocumentsLibrary = ...  # type: UUID
    Downloads = ...  # type: UUID
    Favorites = ...  # type: UUID
    Fonts = ...  # type: UUID
    GameTasks = ...  # type: UUID
    History = ...  # type: UUID
    ImplicitAppShortcuts = ...  # type: UUID
    InternetCache = ...  # type: UUID
    Libraries = ...  # type: UUID
    Links = ...  # type: UUID
    LocalAppData = ...  # type: UUID
    LocalAppDataLow = ...  # type: UUID
    LocalizedResourcesDir = ...  # type: UUID
    Music = ...  # type: UUID
    MusicLibrary = ...  # type: UUID
    NetHood = ...  # type: UUID
    OriginalImages = ...  # type: UUID
    PhotoAlbums = ...  # type: UUID
    PicturesLibrary = ...  # type: UUID
    Pictures = ...  # type: UUID
    Playlists = ...  # type: UUID
    PrintHood = ...  # type: UUID
    Profile = ...  # type: UUID
    ProgramData = ...  # type: UUID
    ProgramFiles = ...  # type: UUID
    ProgramFilesX64 = ...  # type: UUID
    ProgramFilesX86 = ...  # type: UUID
    ProgramFilesCommon = ...  # type: UUID
    ProgramFilesCommonX64 = ...  # type: UUID
    ProgramFilesCommonX86 = ...  # type: UUID
    Programs = ...  # type: UUID
    Public = ...  # type: UUID
    PublicDesktop = ...  # type: UUID
    PublicDocuments = ...  # type: UUID
    PublicDownloads = ...  # type: UUID
    PublicGameTasks = ...  # type: UUID
    PublicLibraries = ...  # type: UUID
    PublicMusic = ...  # type: UUID
    PublicPictures = ...  # type: UUID
    PublicRingtones = ...  # type: UUID
    PublicUserTiles = ...  # type: UUID
    PublicVideos = ...  # type: UUID
    QuickLaunch = ...  # type: UUID
    Recent = ...  # type: UUID
    RecordedTVLibrary = ...  # type: UUID
    ResourceDir = ...  # type: UUID
    Ringtones = ...  # type: UUID
    RoamingAppData = ...  # type: UUID
    RoamedTileImages = ...  # type: UUID
    RoamingTiles = ...  # type: UUID
    SampleMusic = ...  # type: UUID
    SamplePictures = ...  # type: UUID
    SamplePlaylists = ...  # type: UUID
    SampleVideos = ...  # type: UUID
    SavedGames = ...  # type: UUID
    SavedSearches = ...  # type: UUID
    Screenshots = ...  # type: UUID
    SearchHistory = ...  # type: UUID
    SearchTemplates = ...  # type: UUID
    SendTo = ...  # type: UUID
    SidebarDefaultParts = ...  # type: UUID
    SidebarParts = ...  # type: UUID
    SkyDrive = ...  # type: UUID
    SkyDriveCameraRoll = ...  # type: UUID
    SkyDriveDocuments = ...  # type: UUID
    SkyDrivePictures = ...  # type: UUID
    StartMenu = ...  # type: UUID
    Startup = ...  # type: UUID
    System = ...  # type: UUID
    SystemX86 = ...  # type: UUID
    Templates = ...  # type: UUID
    UserPinned = ...  # type: UUID
    UserProfiles = ...  # type: UUID
    UserProgramFiles = ...  # type: UUID
    UserProgramFilesCommon = ...  # type: UUID
    Videos = ...  # type: UUID
    VideosLibrary = ...  # type: UUID
    Windows = ...  # type: UUID


def get_path(folderid: UUID, user_handle: wintypes.HANDLE = ...) -> str: ...
