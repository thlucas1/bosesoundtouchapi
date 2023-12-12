# import all classes from the namespace.
from .addstation import AddStation
from .audiodspcontrols import AudioDspControls, AudioDspAudioModes
from .audioproductlevelcontrols import AudioProductLevelControls
from .audioproducttonecontrols import AudioProductToneControls
from .audiospeakerattributeandsetting import AudioSpeakerAttributeAndSetting
from .balance import Balance
from .bass import Bass
from .basscapabilities import BassCapabilities
from .bluetoothinfo import BlueToothInfo
from .capabilities import Capabilities
from .clockconfig import ClockConfig
from .clocktime import ClockTime
from .contentitem import ContentItem
from .controllevelinfo import ControlLevelInfo
from .dspmonostereoitem import DSPMonoStereoItem
from .group import Group, GroupStatusTypes
from .grouprole import GroupRole, GroupRoleTypes
from .infonetworkconfig import InfoNetworkConfig
from .keystates import KeyStates
from .mediaserverlist import MediaServerList, MediaServer
from .musicserviceaccount import MusicServiceAccount
from .navigate import Navigate, NavigateMenuTypes, NavigateSortTypes
from .navigateresponse import NavigateResponse, NavigateItem
from .networkinfo import NetworkInfo, NetworkInfoInterface
from .networkstatus import NetworkStatus, NetworkStatusInterface
from .nowplayingstatus import NowPlayingStatus
from .performwirelesssitesurveyresponse import PerformWirelessSiteSurveyResponse, SurveyResultItem
from .playinfo import PlayInfo
from .powermanagement import PowerManagement
from .presetlist import PresetList, Preset
from .productcechdmicontrol import ProductCecHdmiControl, ProductCecHdmiModes
from .producthdmiassignmentcontrols import ProductHdmiAssignmentControls
from .rebroadcastlatencymode import RebroadcastLatencyMode
from .recentlist import RecentList, Recent
from .removestation import RemoveStation
from .search import Search, SearchTerm
from .searchfiltertypes import SearchFilterTypes
from .searchresponse import SearchResponse
from .searchresult import SearchResult
from .searchsorttypes import SearchSortTypes
from .searchstation import SearchStation
from .searchstationresults import SearchStationResults, SearchStationSongs, SearchStationArtists
from .serviceAvailability import ServiceAvailability, Service
from .simpleconfig import SimpleConfig
from .softwareupdatecheckresponse import SoftwareUpdateCheckResponse
from .softwareupdatequeryresponse import SoftwareUpdateQueryResponse
from .soundtouchconfigurationstatus import SoundTouchConfigurationStatus
from .sourcelist import SourceList, SourceItem
from .systemtimeout import SystemTimeout
from .trackinfo import TrackInfo
from .volume import Volume
from .wirelessprofile import WirelessProfile
from .zone import Zone, ZoneMember

# all classes to import when "import *" is specified.
__all__ = [
    'AddStation',
    'AudioDspControls', 'AudioDspAudioModes',
    'AudioProductLevelControls',
    'AudioProductToneControls',
    'AudioSpeakerAttributeAndSetting',
    'Balance',
    'Bass',
    'BassCapabilities',
    'BlueToothInfo',
    'Capabilities',
    'ClockConfig',
    'ClockTime',
    'ContentItem',
    'ControlLevelInfo',
    'DSPMonoStereoItem',
    'Group', 'GroupStatusTypes',
    'GroupRole', 'GroupRoleTypes',
    'InfoNetworkConfig',
    'KeyStates',
    'MediaServerList', 'MediaServer',
    'MusicServiceAccount',
    'Navigate', 'NavigateMenuTypes', 'NavigateSortTypes',
    'NavigateResponse', 'NavigateItem',
    'NetworkInfo', 'NetworkInfoInterface',
    'NetworkStatus', 'NetworkStatusInterface',
    'NowPlayingStatus',
    'PerformWirelessSiteSurveyResponse','SurveyResultItem',
    'PlayInfo',
    'PowerManagement',
    'PresetList', 'Preset',
    'ProductCecHdmiControl', 'ProductCecHdmiModes',
    'ProductHdmiAssignmentControls',
    'RebroadcastLatencyMode',
    'RecentList', 'Recent',
    'RemoveStation',
    'Search', 'SearchTerm',
    'SearchFilterTypes',
    'SearchResponse',
    'SearchResult',
    'SearchSortTypes',
    'SearchStation',
    'SearchStationResults', 'SearchStationSongs', 'SearchStationArtists',
    'ServiceAvailability', 'Service',
    'SimpleConfig',
    'SoftwareUpdateCheckResponse',
    'SoftwareUpdateQueryResponse',
    'SoundTouchConfigurationStatus',
    'SourceList', 'SourceItem',
    'SystemTimeout',
    'TrackInfo',
    'Volume',
    'WirelessProfile',
    'Zone', 'ZoneMember'
]
