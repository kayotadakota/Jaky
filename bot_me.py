import vk_api

app_token 		= "47e9d48247e9d48247e9d482a74798dc3f447e947e9d482197d9abd12e45a49ce13b75d"
app_obj			= vk_api.VkApi(token=app_token)
app 			= app_obj.get_api()

print(app.wall.get(domain="vajans"))

