#udacity
Generated using [DbSchema](https://dbschema.com)





<a name='layout1'>### Default Layout
![img](file:/C:/GitHub/Udacity-Data-Engineering-datawarehouse-with-aws-redshift/redshift-udacity/DefaultLayout.svg)






### Table artists 
| Idx | Field Name | Data Type |
|---|---|---|
| 🔍 ⬋ | <a name='public.artists_artist_id'>artist&#95;id</a>| varchar&#40;20&#41; encode lzo |
|  | <a name='public.artists_name'>name</a>| varchar&#40;255&#41; encode lzo |
|  | <a name='public.artists_location'>location</a>| varchar&#40;255&#41; encode lzo |
|  | <a name='public.artists_latitude'>latitude</a>| decimal&#40;18&#44;0&#41; encode az64 |
|  | <a name='public.artists_longitude'>longitude</a>| decimal&#40;18&#44;0&#41; encode az64 |
| Indexes 
| 🔍  | unq&#95;artists&#95;artist&#95;id || ON artist&#95;id|| Options |
| 3 |


### Table songplay 
| Idx | Field Name | Data Type |
|---|---|---|
| *| <a name='public.songplay_songplay_id'>songplay&#95;id</a>| integer  DEFAULT "identity"(118240, 0, '0,1'::text) |
| *⬈ | <a name='public.songplay_start_time'>start&#95;time</a>| timestamp encode az64 |
| *⬈ | <a name='public.songplay_user_id'>user&#95;id</a>| integer encode az64 |
|  | <a name='public.songplay_level'>level</a>| varchar&#40;20&#41; encode lzo |
| *⬈ | <a name='public.songplay_song_id'>song&#95;id</a>| varchar&#40;20&#41; encode lzo |
| *⬈ | <a name='public.songplay_artist_id'>artist&#95;id</a>| varchar&#40;20&#41; encode lzo |
| *| <a name='public.songplay_session_id'>session&#95;id</a>| integer encode az64 |
|  | <a name='public.songplay_location'>location</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.songplay_user_agent'>user&#95;agent</a>| varchar&#40;256&#41; encode lzo |
| Indexes 
| 🔎  | Sorting || ON songplay&#95;id|| Foreign Keys |  | fk_songplay_time | ( start&#95;time ) ref [public&#46;time](#time) (start&#95;time) 
||  | fk_songplay_songs | ( song&#95;id ) ref [public&#46;songs](#songs) (song&#95;id) 
||  | fk_songplay_artists | ( artist&#95;id ) ref [public&#46;artists](#artists) (artist&#95;id) 
||  | fk_songplay_users | ( user&#95;id ) ref [public&#46;users](#users) (level) 
|| Options |
| 3 |


### Table songs 
| Idx | Field Name | Data Type |
|---|---|---|
| 🔍 ⬋ | <a name='public.songs_song_id'>song&#95;id</a>| varchar&#40;20&#41; encode lzo |
|  | <a name='public.songs_title'>title</a>| varchar&#40;255&#41; encode lzo |
|  | <a name='public.songs_artist_id'>artist&#95;id</a>| varchar&#40;20&#41; encode lzo |
|  | <a name='public.songs_duration'>duration</a>| decimal&#40;18&#44;0&#41; encode az64 |
|  | <a name='public.songs_year'>year</a>| integer encode az64 |
| Indexes 
| 🔍  | unq&#95;songs&#95;song&#95;id || ON song&#95;id|| Options |
| 3 |


### Table staging_events 
| Idx | Field Name | Data Type |
|---|---|---|
|  | <a name='public.staging_events_artist'>artist</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_auth'>auth</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_firstname'>firstname</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_gender'>gender</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_iteminsession'>iteminsession</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_lastname'>lastname</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_length'>length</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_level'>level</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_location'>location</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_method'>method</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_page'>page</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_registration'>registration</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_sessionid'>sessionid</a>| integer encode az64 |
|  | <a name='public.staging_events_song'>song</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_status'>status</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_ts'>ts</a>| bigint encode az64 |
|  | <a name='public.staging_events_useragent'>useragent</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_events_userid'>userid</a>| integer encode az64 |
| Options |
| 3 |


### Table staging_songs 
| Idx | Field Name | Data Type |
|---|---|---|
|  | <a name='public.staging_songs_num_songs'>num&#95;songs</a>| integer encode az64 |
|  | <a name='public.staging_songs_artist_id'>artist&#95;id</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_artist_latitude'>artist&#95;latitude</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_artist_longitude'>artist&#95;longitude</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_artist_location'>artist&#95;location</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_artist_name'>artist&#95;name</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_song_id'>song&#95;id</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_title'>title</a>| varchar&#40;256&#41; encode lzo |
|  | <a name='public.staging_songs_duration'>duration</a>| decimal&#40;18&#44;0&#41; encode az64 |
|  | <a name='public.staging_songs_year'>year</a>| integer encode az64 |
| Options |
| 3 |


### Table time 
| Idx | Field Name | Data Type |
|---|---|---|
| *🔍 ⬋ | <a name='public.time_start_time'>start&#95;time</a>| timestamp  |
|  | <a name='public.time_hour'>hour</a>| integer encode az64 |
|  | <a name='public.time_day'>day</a>| integer encode az64 |
|  | <a name='public.time_week'>week</a>| integer encode az64 |
|  | <a name='public.time_month'>month</a>| integer encode az64 |
|  | <a name='public.time_year'>year</a>| integer encode az64 |
|  | <a name='public.time_weekday'>weekday</a>| integer encode az64 |
| Indexes 
| 🔍  | Sorting || ON start&#95;time|| Options |
| 3 |


### Table users 
| Idx | Field Name | Data Type |
|---|---|---|
| *🔍 | <a name='public.users_user_id'>user&#95;id</a>| integer  |
|  | <a name='public.users_first_name'>first&#95;name</a>| varchar&#40;255&#41; encode lzo |
|  | <a name='public.users_last_name'>last&#95;name</a>| varchar&#40;255&#41; encode lzo |
|  | <a name='public.users_gender'>gender</a>| varchar&#40;1&#41; encode lzo |
| 🔍 ⬋ | <a name='public.users_level'>level</a>| varchar&#40;20&#41; encode lzo |
| Indexes 
| 🔍  | Sorting || ON user&#95;id|| 🔍  | unq&#95;users&#95;level || ON level|| Options |
| 3 |





