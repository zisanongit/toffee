import requests
import json
import uuid

# Toffee Official Android Media3 Headers
TOFFEE_HEADERS = {
    "User-Agent": "Toffee (Linux;Android 14) AndroidXMedia3/1.1.1/64100410/4d2ec9b8c3502383",
    "Origin": "https://toffeelive.com",
    "Referer": "https://toffeelive.com/",
    "Accept": "*/*"
}

# আপনার ৭৬টি চ্যানেলের তালিকা (সরাসরি টুফি সিডিএন পাথের সাথে)
CHANNELS = [
    {"id": "toffee_drama", "name": "Toffee TV", "group": "Family", "path": "cdn/live/toffee_drama/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/DNMXs5UBm1RY_In7IJ72/posters/737b5c6e-8435-4cd8-81de-16a499fa6f4e.png"},
    {"id": "toffee_movie", "name": "Toffee Movies", "group": "Movies", "path": "cdn/live/toffee_movie/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/b60Ss5UBrjBfS2_RJPb8/posters/c68ede73-0be0-41b7-9130-9628a16f2feb.png"},
    {"id": "epl_1", "name": "EPL channel 1", "group": "Live Action", "path": "live/EPL-26-27-CH-1/index.m3u8", "logo": "https://assets-prod.services.toffeelive.com/JS1AqZgBNnOkwJLWlwg-/posters/f030066c-0649-4d82-836f-c85321381d67.png"},
    {"id": "bfl_1", "name": "BFL | Live 1", "group": "Sports", "path": "live/BFFL-1/index.m3u8", "logo": "https://assets-prod.services.toffeelive.com/HHnAgJkBcqxnFHJBabwO/posters/967dd1fe-c2af-442e-a0b1-22320ed82c88.png"},
    {"id": "fifa_wc", "name": "WC Match Recap", "group": "Sports", "path": "cdn/live/fifa_world_cup/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/V__o054BObUt2AG6LL5C/posters/84590b8d-6430-4ba8-a0a5-757bf2f57c05.png"},
    {"id": "cnn", "name": "CNN", "group": "Documentary", "path": "cdn/live/cnn/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/VC6Q-JQBv9knK3AHhTXt/posters/63e79814-8fcf-4c3e-bb66-408b2a402613.webp"},
    {"id": "somoy_tv", "name": "Somoy TV", "group": "Live Action", "path": "cdn/live/somoy_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Xi_Ga5oBNnOkwJLWkhKP/posters/ef2899d5-1ae0-4fee-aee5-45f9b0b3ba80.png"},
    {"id": "jamuna_tv", "name": "Jamuna TV", "group": "Live Action", "path": "cdn/live/jamuna_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/PiL635oBEef-9-uV2uCe/posters/36f380e0-6c71-4b27-a73b-2afb3ce7e982.png"},
    {"id": "anandatv", "name": "Ananda TV", "group": "Live Action", "path": "cdn/live/anandatv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/wCM3l5sBEef-9-uVXFvD/posters/d80f7aee-5bd7-4edc-97eb-ead0e3ebbe09.png"},
    {"id": "bijoytv", "name": "Bijoy TV", "group": "Action", "path": "cdn/live/bijoytv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/bns4l5sBcqxnFHJBVZ32/posters/feaf9f3d-cc3b-4a3d-81a3-2cb703e561eb.png"},
    {"id": "n_tv", "name": "NTV", "group": "Live Action", "path": "cdn/live/n_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/wHLVIJ4B7a1HdMSjaGLJ/posters/83b89557-3ae8-4ca8-8c5d-3c617359c738.png"},
    {"id": "globaltv", "name": "Global TV", "group": "Live Action", "path": "cdn/live/globaltv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/0y_tDJsBNnOkwJLWNrdE/posters/2ff058e1-630f-4657-8dc6-b677e65642c5.png"},
    {"id": "channel_s_tv", "name": "Channel S", "group": "Live Action", "path": "cdn/live/channel_s_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/WyPuDJsBEef-9-uVUA_z/posters/ea20055c-a824-443c-8083-ce8e2da8b922.png"},
    {"id": "rajdhani_tv", "name": "Rajdhani TV", "group": "Live Action", "path": "cdn/live/rajdhani_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/KECGB54BuUSiBsg_dHyj/posters/58af9c58-ed80-458c-af13-cf381680cec6.png"},
    {"id": "bangla_tv", "name": "Bangla TV", "group": "Live Action", "path": "cdn/live/bangla_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/JiK-_poBEef-9-uVZv6L/posters/757a328e-70d6-45de-b093-0a843c69ade7.png"},
    {"id": "asian_tv", "name": "Asian TV", "group": "Live Action", "path": "cdn/live/asian_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/MyK__poBEef-9-uVmf5l/posters/1eadef5b-28e7-4dc2-b42f-c67a3357c9a0.png"},
    {"id": "channel_i", "name": "Channel i", "group": "Live Action", "path": "cdn/live/channel_i/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/qnv835oBcqxnFHJBuQcB/posters/348dfac3-c1e0-485d-a72b-3d282c9e2c73.png"},
    {"id": "movie_bangla", "name": "Movie Bangla", "group": "Live Action", "path": "cdn/live/movie_bangla/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/CXz4PJwBcqxnFHJBPwrG/posters/2f913e34-3a6c-45e6-9f1f-97bf129a2ff5.png"},
    {"id": "nexus_tv", "name": "Nexus TV", "group": "Live Action", "path": "cdn/live/nexus_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/FHz5PJwBcqxnFHJBdAqW/posters/419869ac-8ddf-4909-86c1-b69f0a3adf13.png"},
    {"id": "islamic_tv", "name": "Islamic TV", "group": "Live Action", "path": "cdn/live/islamic_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/jehEA54BIxFjn23xAmdw/posters/2c276556-cbcd-4467-b627-4394bb20f250.png"},
    {"id": "desh_tv", "name": "Desh TV", "group": "Live Action", "path": "cdn/live/desh_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/6Hz1PJwBcqxnFHJBhgkV/posters/845f1e3f-987a-47cc-a48d-ee12d8f4d419.png"},
    {"id": "independent_tv", "name": "Independent TV", "group": "Live Action", "path": "cdn/live/independent_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ES_cZZsBNnOkwJLW1Oz1/posters/b872b8f5-cb6b-45a1-a1cd-7609df51d614.png"},
    {"id": "ekhon_tv", "name": "Ekhon TV", "group": "Live Action", "path": "cdn/live/ekhon_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/o3v235oBcqxnFHJBkAdC/posters/159af631-796d-4342-a2a7-c272f32bcd32.png"},
    {"id": "ekattor_tv", "name": "Ekattor TV", "group": "Live Action", "path": "cdn/live/ekattor_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/PS_La5oBNnOkwJLWLRN_/posters/e8c444fd-ee3b-4bf3-bb0a-f969bc295f82.png"},
    {"id": "channels_news_asia", "name": "Channel News Asia", "group": "Documentary", "path": "cdn/live/channels_news_asia/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/rYOv_p8BJIOHmUelrnXh/posters/d537453f-7e5b-45f3-9b52-42f6f65950c8.png"},
    {"id": "trt_world", "name": "TRT World", "group": "Documentary", "path": "cdn/live/trt_world/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/1YPq_p8BJIOHmUelSHXc/posters/f65b0273-0f23-4b56-93dd-417224369105.png"},
    {"id": "dw_tv", "name": "DW", "group": "Documentary", "path": "cdn/live/dw_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/7oPt_p8BJIOHmUelhXWj/posters/d6328092-9437-4806-8dc7-d00732d56832.png"},
    {"id": "russia_today", "name": "Russia Today", "group": "Documentary", "path": "cdn/live/russia_today/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/CNT2_p8BalKyvLQIBSUG/posters/1e937055-a014-4274-bb69-b1b56d18c434.png"},
    {"id": "france_24", "name": "France 24", "group": "Documentary", "path": "cdn/live/france_24/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/G4ML_58BJIOHmUelNXZr/posters/becc2fba-4ed5-4f43-af2d-3c1ea2b4ee57.png"},
    {"id": "cgtn", "name": "CGTN", "group": "Documentary", "path": "cdn/live/cgtn/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/DYMI_58BJIOHmUelm3aK/posters/d8436322-804a-47b6-9a3f-62764c4622d5.png"},
    {"id": "euro_sports_hd", "name": "Eurosport HD", "group": "Sports", "path": "cdn/live/euro_sports_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Uy6Q-JQBv9knK3AHcDUQ/posters/01709bcd-6d53-4710-a64f-bc49cecf1d61.webp"},
    {"id": "saudi_sunnah", "name": "Saudi Sunnah", "group": "Documentary", "path": "cdn/live/saudi_sunnah/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/JNQA_58BalKyvLQIhiVD/posters/11e764bf-7969-4dcb-a94c-937a3bde2a7f.png"},
    {"id": "saudi_quran", "name": "Saudi Quran", "group": "Documentary", "path": "cdn/live/saudi_quran/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/FdT9_p8BalKyvLQIpCUP/posters/6b39f2c6-6fe8-4720-a986-379e09968b5b.png"},
    {"id": "sony_sports_1_hd", "name": "Sony Ten Sports 1 HD", "group": "Sports", "path": "cdn/live/sony_sports_1_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/py5j-JQBv9knK3AHxDTY/posters/ea3358b9-2bec-4615-a889-daa2e396c74c.webp"},
    {"id": "sony_sports_2_hd", "name": "Sony Ten Sports 2 HD", "group": "Sports", "path": "cdn/live/sony_sports_2_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/sy5m-JQBv9knK3AHYTTk/posters/5e40bf0e-633f-4d37-a3b2-3d606f0ac19a.png"},
    {"id": "sony_sports_5_hd", "name": "Sony Ten Sports 5 HD ", "group": "Sports", "path": "cdn/live/sony_sports_5_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/vi5n-JQBv9knK3AHqzTC/posters/d171fd4d-0369-4213-b0c5-e241974f5459.png"},
    {"id": "ten_cricket", "name": "Sony Ten Cricket", "group": "Sports", "path": "cdn/live/ten_cricket/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ra2x_pQBrjBfS2_RWG9l/posters/795170c2-ec78-457e-9fa0-54a23d23361c.webp"},
    {"id": "cartoon_network_hd", "name": "Cartoon Network HD +", "group": "Teen", "path": "cdn/live/cartoon_network_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/1y6e-JQBv9knK3AHNDWb/posters/ee9ba01b-1bcf-436b-b273-7b857f0810fb.webp"},
    {"id": "cartoon_network_sd", "name": "Cartoon Network", "group": "Teen", "path": "cdn/live/cartoon_network_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/mC6W-JQBv9knK3AHfDWA/posters/d2a02d82-fde4-4769-a6d9-95c0560e2120.webp"},
    {"id": "pogo_sd", "name": "POGO", "group": "Teen", "path": "cdn/live/pogo_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ny6W-JQBv9knK3AHujXC/posters/7e7c2afe-a663-4c09-983a-2d0fa0f1ca9a.webp"},
    {"id": "discovery_kids", "name": "Discovery Kids", "group": "Teen", "path": "cdn/live/discovery_kids/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/1i6e-JQBv9knK3AHHTXR/posters/325887a7-84ea-4cf9-a6fd-6111ddc25671.webp"},
    {"id": "sonyyay", "name": "Sony YAY", "group": "Family", "path": "cdn/live/sonyyay/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/IC5_-JQBv9knK3AHFDXh/posters/36df4012-80f2-4a98-9970-3b663f62093f.webp"},
    {"id": "zee_bangla", "name": "Zee Bangla", "group": "Drama", "path": "cdn/live/zee_bangla/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/kK2aX5UBrjBfS2_RBcKf/posters/ba5dd8dc-4f87-414a-b57f-c9ecdeda5253.png"},
    {"id": "zee_anmol", "name": "Zee Anmol", "group": "Drama", "path": "cdn/live/zee_anmol/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/7x0Jd5YBEef-9-uVv_Gy/posters/f9c07bfc-9fde-40d0-91a1-e28c5840f400.png"},
    {"id": "zing_sd", "name": "Zing", "group": "Comedy", "path": "cdn/live/zing_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/DK8dd5YBrjBfS2_Ru22e/posters/a4e57fd0-1853-4540-a9bc-0265ee43b5cb.png"},
    {"id": "hum_tv", "name": "HUM", "group": "Drama", "path": "cdn/live/hum_tv/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/0C63X5UBv9knK3AHxaOs/posters/6dce1143-1045-4fec-ac4f-86d2bfb32447.png"},
    {"id": "hum_masala", "name": "HUM Masala", "group": "Drama", "path": "cdn/live/hum_masala/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/T9O9X5UBm1RY_In7UXFv/posters/30e0f372-eb3e-4cf9-be1e-b196a40c2fc7.png"},
    {"id": "hum_sitaray", "name": "HUM Sitaray", "group": "Drama", "path": "cdn/live/hum_sitaray/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/WtPBX5UBm1RY_In7mXEU/posters/188d51f6-aeef-41ed-835b-e25ff911e209.png"},
    {"id": "sonyaath", "name": "Sony Aath", "group": "Drama", "path": "cdn/live/sonyaath/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/xi6xX5UBv9knK3AH9aMk/posters/f4db1c12-b10f-46e8-a09b-e0efb8820970.png"},
    {"id": "sonyentertainmnt_hd", "name": "Sony Entertainment Television HD", "group": "Family", "path": "cdn/live/sonyentertainmnt_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/-y50-JQBv9knK3AHLzSn/posters/0ab48ac0-ec84-4ca2-9601-746ff3cb809e.webp"},
    {"id": "sony_entertainment", "name": "Sony Entertainment Television", "group": "Family", "path": "cdn/live/sony_entertainment/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/2S5t-JQBv9knK3AHJTTW/posters/ae74f943-77c9-4395-a16c-8ed84b439080.webp"},
    {"id": "b4u_music", "name": "B4U Music", "group": "Musical", "path": "cdn/live/b4u_music/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/PS6F-JQBv9knK3AHqjVz/posters/0f83ee72-be0f-4861-94df-30b158d3df8d.webp"},
    {"id": "sonysab_hd", "name": "Sony SAB HD", "group": "Family", "path": "cdn/live/sonysab_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ES55-JQBv9knK3AHNDWC/posters/13411be9-62b9-4a99-a062-b6e91dfb1099.webp"},
    {"id": "zee_tv_hd", "name": "Zee TV HD", "group": "Drama", "path": "cdn/live/zee_tv_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ltPQX5UBm1RY_In7b3F1/posters/d039d9df-9877-4969-a0b6-56888ebe2385.png"},
    {"id": "sony_max_hd", "name": "Sony MAX HD", "group": "Movies", "path": "cdn/live/sony_max_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ai51-JQBv9knK3AH_jWs/posters/663e52a6-1a9f-4458-b4aa-7c03d84972f1.webp"},
    {"id": "zee_bangla_cinema", "name": "Zee Bangla Cinema", "group": "Movies", "path": "cdn/live/zee_bangla_cinema/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/-C7MX5UBv9knK3AHdKOi/posters/e37fef13-9bf3-4ecc-8b74-fca091874fa0.png"},
    {"id": "zee_bollywood", "name": "Zee Bollywood", "group": "Movies", "path": "cdn/live/zee_bollywood/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/OnSlPJYBcqxnFHJB6lFX/posters/d9ccb2a6-227f-4a41-8714-efaddab5cf5e.png"},
    {"id": "zee_action", "name": "Zee Action", "group": "Movies", "path": "cdn/live/zee_action/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Pc3RD5YBtpl-Sbt7doxr/posters/33d667ae-bcc3-4f6b-b376-76c552136923.png"},
    {"id": "sony_max", "name": "Sony MAX", "group": "Movies", "path": "cdn/live/sony_max/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ay52-JQBv9knK3AHFDWt/posters/00afb30b-3c19-4c4c-abd8-891db94e4767.webp"},
    {"id": "sonypix_hd", "name": "Sony PIX HD", "group": "Movies", "path": "cdn/live/sonypix_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ly6C-JQBv9knK3AHOjXt/posters/252e64ca-8d99-46e7-a951-e10c1703c11d.webp"},
    {"id": "zee_cafe_hd", "name": "Zee Cafe", "group": "Movies", "path": "cdn/live/zee_cafe_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/U3QEd5YBcqxnFHJBpYzc/posters/8bc7ae1b-1a46-4b76-bdb1-13c7dbd3a95c.png"},
    {"id": "b4u_movies", "name": "B4U Movies APAC", "group": "Movies", "path": "cdn/live/b4u_movies/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/PC6F-JQBv9knK3AHlTUO/posters/fb0243ba-39a0-4101-a78c-c197be550c6c.webp"},
    {"id": "sonymax_2", "name": "Sony MAX 2", "group": "Movies", "path": "cdn/live/sonymax_2/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ii5_-JQBv9knK3AHLDV3/posters/d961cc87-81b6-4b30-8414-8c0af2774818.webp"},
    {"id": "zee_cinema_hd", "name": "Zee Cinema HD", "group": "Movies", "path": "cdn/live/zee_cinema_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/5y7HX5UBv9knK3AHs6Nk/posters/7582fb79-c15f-4247-ba5b-1d2dd27f3d71.png"},
    {"id": "tlc_hd", "name": "TLC HD", "group": "Fantasy", "path": "cdn/live/tlc_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/7S6j-JQBv9knK3AHbzXC/posters/0973097c-bc5c-4b28-aaca-f04d6f6cb5e2.webp"},
    {"id": "tlc_sd", "name": "TLC", "group": "Fantasy", "path": "cdn/live/tlc_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/7C6j-JQBv9knK3AHVzUA/posters/e8f84105-5efe-4e91-a0d4-18a0849cf2f2.webp"},
    {"id": "animal_planet_sd", "name": "Animal Planet", "group": "Adventure", "path": "cdn/live/animal_planet_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ny61-JQBv9knK3AHgzZ7/posters/0909b36a-afd5-426a-93b3-4512800977db.webp"},
    {"id": "animal_planet_hd", "name": "Animal Planet HD", "group": "Adventure", "path": "cdn/live/animal_planet_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ni61-JQBv9knK3AHcDYc/posters/c16e8633-6b2a-401a-9cd6-ac26a4fcdedb.webp"},
    {"id": "sonybbc_earth_hd", "name": "Sony BBC Earth HD", "group": "Family", "path": "cdn/live/sonybbc_earth_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/MC6C-JQBv9knK3AHUzUT/posters/a8c32fd3-2ba7-437c-85ac-de2f1b2fa6ca.webp"},
    {"id": "discovery_hd", "name": "Discovery HD", "group": "Adventure", "path": "cdn/live/discovery_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/KC6x-JQBv9knK3AHqjYc/posters/55e554f1-dbbb-47bd-97fe-fca878726c4c.webp"},
    {"id": "discovery_sd", "name": "Discovery", "group": "Adventure", "path": "cdn/live/discovery_sd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/KS6x-JQBv9knK3AHwDZy/posters/6594d216-aaca-4eee-b6f5-bbc6b80feb15.webp"},
    {"id": "discovery_science", "name": "Discovery Science", "group": "Science Fiction", "path": "cdn/live/discovery_science/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/AS6s-JQBv9knK3AHDTZb/posters/eab8fd0f-9351-464c-b45e-332f38b49f4b.webp"},
    {"id": "discovery_turbo", "name": "Discovery Turbo", "group": "Adventure", "path": "cdn/live/discovery_turbo/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/Ay6s-JQBv9knK3AHJTY1/posters/e8f65578-e82d-4e4a-a1ff-073becc5bd71.webp"},
    {"id": "discovary_investigation_hd", "name": "Investigation Discovery HD", "group": "Documentary", "path": "cdn/live/discovary_investigation_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/ay7uX5UBv9knK3AHs6TI/posters/deb3c186-b2e1-4a91-aafb-d86f9128b851.png"},
    {"id": "and_tv_hd", "name": "&TV HD", "group": "Drama", "path": "cdn/live/and_tv_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/5cwRnZUBtpl-Sbt7wWrN/posters/5779ade3-e9ba-4107-b3da-bae6f891500a.png"},
    {"id": "andpicture_hd", "name": "& Pictures HD", "group": "Movies", "path": "cdn/live/andpicture_hd/playlist.m3u8", "logo": "https://assets-prod.services.toffeelive.com/QMwWnZUBtpl-Sbt7S2sx/posters/8cad9a82-842a-47bf-a060-f17011f11c07.png"}
]

# সরাসরি টুফি অফিশিয়াল সার্ভার থেকে তাজা টোকেন লিংক তুলে আনার ফাংশন
def fetch_fresh_token_url(channel_path):
    device_id = str(uuid.uuid4())
    headers = dict(TOFFEE_HEADERS)
    headers["X-Device-Id"] = device_id
    headers["X-Session-Token"] = device_id
    
    url = f"https://prod-linear-media.toffeelive.com/{channel_path}"
    try:
        session = requests.Session()
        res = session.get(url, headers=headers, allow_redirects=True, timeout=12)
        if res.ok or res.status_code == 302:
            return res.url if res.url else url
    except Exception as e:
        print(f"Error fetching {channel_path}: {e}")
    return url

def main():
    print("Generating fresh Toffee tokens directly from Toffee official gateway...")
    m3u_lines = ["#EXTM3U"]
    for ch in CHANNELS:
        fresh_url = fetch_fresh_token_url(ch["path"])
        m3u_lines.append(f'#EXTINF:-1 tvg-id="{ch["id"]}" tvg-name="{ch["name"]}" tvg-logo="{ch["logo"]}" group-title="{ch["group"]}",{ch["name"]}')
        m3u_lines.append(fresh_url)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    print(f"SUCCESS: Generated playlist.m3u with {len(CHANNELS)} fresh channel tokens!")

if __name__ == "__main__":
    main()
