import requests
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - %(message)s')

class ApiClient:
    def __init__(self):
        self.base_url = 'https://jsonplaceholder.typicode.com'
        self.headers = {'Content-Type': 'application/json'}

    def _request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        try:
            response = requests.request(method, url, json=data, headers=self.headers)
            if response.status_code in (200, 201):
                logging.info(f'Запрос {method} на {url} завершился успешно {response.status_code} {response.reason}')
                return response.json()
            else:
                logging.error(f'Сервер вернул ошибку {response.status_code} {response.reason} для {method} на {url}')
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f'Сетевая ошибка при запросе {method} на {url}: {e}')
            return None

    def get(self, endpoint):
        return self._request('GET', endpoint)

    def post(self, endpoint, data):
        return self._request('POST', endpoint, data)

    def put(self, endpoint, data):
        return self._request('PUT', endpoint, data)

    def patch(self, endpoint, data):
        return self._request('PATCH', endpoint, data)

    def delete(self, endpoint):
        return self._request('DELETE', endpoint)


def main():
    client = ApiClient()
    # GET
    response = client.get('/posts')
    if response:
        logging.info(f'Кол-во постов: {len(response)}')
    # POST
    post_data = {'title': 'THIS IS TITLE', 'body': 'THIS IS BODY', 'userId': 999}
    post_response = client.post('/posts', data=post_data)
    if post_response:
        logging.info(f'Данные поста: {post_response}')
    # PUT
    put_data = {'title': 'UPDATED TITLE', 'body': 'UPDATED BODY', 'userId': 1, 'id': 1}
    put_response = client.put('/posts/1', data=put_data)
    if put_response:
        logging.info(f'Данные после PUT {put_response}')
    # PATCH
    patch_data = {'title': 'PATCH TITLE'}
    patch_response = client.patch('/posts/1', data=patch_data)
    if patch_response:
        logging.info(f'Данные после PAtCH {patch_response}')
    # DELETE
    client.delete('/posts/1')



if __name__ == '__main__':
    main()