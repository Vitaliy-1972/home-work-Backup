import requests
from pprint import pprint


class VK:
    api_base_url = 'https://api.vk.com/method'

    def __init__(self, token, user_id, album_id):
        self.token = token
        self.owner_id = owner_id
        self.album_id = album_id

    def get_common_params(self):
        return {
            'access_token': self.token,
            'v': '5.199',
            'owner_id': self.owner_id,
            'album_id': self.album_id,
            'extended': 1,
            'count': 5
        }

    def get_users_photo(self):
        params = self.get_common_params()
        response = requests.get(f'{self.api_base_url}/photos.get', params=params)
        # return  response.json()
        return response.json()['response']['items']


    def loading_photo_to_yandex_disk(self):
        headers = {
            'Authorization': 'token yandex_disk'
        }
        response = requests.put('https://cloud-api.yandex.net/v1/disk/resources',
                                headers=headers,
                                params={'path': 'Backups'}, )
        for photos in self.get_users_photo():
            date = photos['date']
            likes = photos['likes']['count']
            for photo in photos['sizes']:
                if photo['type'] == 'w':
                    photo_url = photo['url']
                    image_name = f'{likes}_{date}'
                    params = {
                    'url':f'{photo_url}',
                    'path': f'Backups/{likes}_{date}'
                     }
                    response = requests.post('https://cloud-api.yandex.net/v1/disk/resources/upload',
                                         headers=headers,
                                         params=params)
                    print(f'Фотография {likes}_{date} загрузилась на яндекс диск')
        print('Копирование завершено')


access_token = ('token VK')
owner_id = 800082799
album_id = 302291822
vk = VK(access_token, owner_id, album_id)

if __name__ == '__main__':
    vk.loading_photo_to_yandex_disk()

