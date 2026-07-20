import requests
import logging

from exceptions import JSONPlaceholderServerError

logging.basicConfig(level=logging.INFO, format='[%(name)s] - %(asctime)s - [%(levelname)s] - %(message)s')
logger = logging.getLogger(__name__)

class ApiClient:
    def __init__(self):
        self.base_url = 'https://jsonplaceholder.typicode.com'
        self.headers = {'Content-Type': 'application/json'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _request(self, method, endpoint, data=None):
        url = self.base_url + endpoint
        try:
            response = self.session.request(method, url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            logger.info(f'Запрос {method} на {url} завершился успешно {response.status_code} {response.reason}')
            try:
                result = response.json()
            except requests.exceptions.JSONDecodeError as e:
                logger.error(f'Сервер вернул ошибку {response.status_code} {response.reason} для {method} на {url}: {e}')
                raise JSONPlaceholderServerError from e
        except requests.exceptions.RequestException as e:
            logger.error(f'Сетевая ошибка при запросе {method} на {url}: {e}')
            raise JSONPlaceholderServerError from e
        return result

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
        logger.info(f'Кол-во постов: {len(response)}')
    # POST
    post_data = {'title': 'THIS IS TITLE', 'body': 'THIS IS BODY', 'userId': 999}
    post_response = client.post('/posts', data=post_data)
    if post_response:
        logger.info(f'Данные поста: {post_response}')
    # PUT
    put_data = {'title': 'UPDATED TITLE', 'body': 'UPDATED BODY', 'userId': 1, 'id': 1}
    put_response = client.put('/posts/1', data=put_data)
    if put_response:
        logger.info(f'Данные после PUT {put_response}')
    # PATCH
    patch_data = {'title': 'PATCH TITLE'}
    patch_response = client.patch('/posts/1', data=patch_data)
    if patch_response:
        logger.info(f'Данные после PAtCH {patch_response}')
    # DELETE
    client.delete('/posts/1')



if __name__ == '__main__':
    main()