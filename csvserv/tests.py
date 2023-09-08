from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from users.models import User


class UserTestCase(APITestCase):
    """Test for UserCreateView"""
    def setUp(self):
        self.userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }

    def test_user_create(self):
        """Create a new user"""
        response = self.client.post(
            reverse('users:create_user'),
            data=self.userdata
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_user_token_create(self):
        """Get token"""
        user = User.objects.create(
            email=self.userdata.get('email'),
            is_active=True
        )
        user.set_password(self.userdata.get('password'))
        user.save()
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            self.userdata
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_user_token_refresh(self):
        """Refresh token"""
        user = User.objects.create(
            email=self.userdata.get('email'),
            is_active=True
        )
        user.set_password(self.userdata.get('password'))
        user.save()
        tokens = self.client.post(
            reverse('users:token_obtain_pair'),
            self.userdata
        )
        response = self.client.post(
            reverse('users:token_refresh'),
            {'refresh': tokens.json().get('refresh')}
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )


class CsvTestCase(APITestCase):
    """Test for CsvCreateView"""
    def setUp(self):
        """Fill database before tests are run"""
        self.userdata = {
            'email': 'test@test.ru',
            'password': '12345',
        }
        user = User.objects.create(
            email=self.userdata.get('email'),
            is_active=True
        )
        user.set_password(self.userdata.get('password'))
        user.save()
        response = self.client.post(
            reverse('users:token_obtain_pair'),
            self.userdata
        )
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.json().get('access'))

    def test_file_upload(self):
        """Upload a file"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

    def test_file_delete(self):
        """Upload and delete a file"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        response = self.client.delete(
        reverse('csvserv:delete', kwargs={'pk': response.json().get('id')})
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_files_list(self):
        """Get files list with fields"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        id = response.json().get('id')
        response = self.client.get(reverse('csvserv:list'))

        self.assertEqual(
            [{
                'id': id,
                'file_name': 'test_file.csv',
                'file_fields': [
                    'Poster_Link',
                    'Series_Title',
                    'Released_Year',
                    'Certificate',
                    'Runtime',
                    'Genre',
                    'IMDB_Rating',
                    'Overview',
                    'Meta_score',
                    'Director',
                    'Star1',
                    'Star2',
                    'Star3',
                    'Star4',
                    'No_of_Votes',
                    'Gross']
            }],
            response.json()
        )
