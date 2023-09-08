import json

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

    def test_files_detail(self):
        """Test getting file data using sort and filter"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        id = response.json().get('id')
        data = {
            "sort": {
                "Released_Year": False,
                "IMDB_Rating": True
            },
            "filter": {
                "Genre": "Drama",
                "Meta_score": "77",
                "Certificate": "R"
            }
        }
        response = self.client.generic(
            method="GET",
            path=reverse('csvserv:detail', kwargs={'pk': id}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(
            {
                "id": id,
                "file_name": "test_file.csv",
                "file_fields": [
                    {
                        "Poster_Link": "https://m.media-amazon.com/images/M/MV5BMTg2NDg3ODg4NF5BMl5BanBnXkFtZTcwNzk3NTc3Nw@@._V1_UY98_CR1,0,67,98_AL_.jpg",
                        "Series_Title": "Jagten",
                        "Released_Year": "2012",
                        "Certificate": "R",
                        "Runtime": "115 min",
                        "Genre": "Drama",
                        "IMDB_Rating": "8.3",
                        "Overview": "A teacher lives a lonely life, all the while struggling over his son's custody. His life slowly gets better as he finds love and receives good news from his son, but his new luck is about to be brutally shattered by an innocent little lie.",
                        "Meta_score": "77",
                        "Director": "Thomas Vinterberg",
                        "Star1": "Mads Mikkelsen",
                        "Star2": "Thomas Bo Larsen",
                        "Star3": "Annika Wedderkopp",
                        "Star4": "Lasse Fogelstrøm",
                        "No_of_Votes": "281623",
                        "Gross": "687,185"
                    },
                    {
                        "Poster_Link": "https://m.media-amazon.com/images/M/MV5BZjk3YThkNDktNjZjMS00MTBiLTllNTAtYzkzMTU0N2QwYjJjXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX67_CR0,0,67,98_AL_.jpg",
                        "Series_Title": "Magnolia",
                        "Released_Year": "1999",
                        "Certificate": "R",
                        "Runtime": "188 min",
                        "Genre": "Drama",
                        "IMDB_Rating": "8",
                        "Overview": "An epic mosaic of interrelated characters in search of love, forgiveness, and meaning in the San Fernando Valley.",
                        "Meta_score": "77",
                        "Director": "Paul Thomas Anderson",
                        "Star1": "Tom Cruise",
                        "Star2": "Jason Robards",
                        "Star3": "Julianne Moore",
                        "Star4": "Philip Seymour Hoffman",
                        "No_of_Votes": "289742",
                        "Gross": "22,455,976"
                    }
                ]
            },
            response.json()
        )

    def test_files_detail_with_wrong_sort(self):
        """Test getting data using wrong sort params"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        id = response.json().get('id')
        data = {
            "sort": {
                "Released_Year": "qwerty",
                "IMDB_Rating": True
            },
            "filter": {
                "Genre": "Drama",
                "Meta_score": "77",
                "Certificate": "R"
            }
        }
        response = self.client.generic(
            method="GET",
            path=reverse('csvserv:detail', kwargs={'pk': id}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(
            {
                'id': id,
                'file_name': 'test_file.csv',
                'file_fields': {
                    'Released_Year': 'value of this field can be only false or true'
                }
            },
            response.json()
        )

    def test_files_detail_with_wrong_filter(self):
        """Test getting data using wrong filter params"""
        with open('test_file.csv', 'rb') as fp:
            response = self.client.post(reverse('csvserv:upload'),
                                        {'file': fp},
                                        format='multipart')
        id = response.json().get('id')
        data = {
            "sort": {
                "Released_Year": False,
                "IMDB_Rating": True
            },
            "filter": {
                "GenreQQQ": "Drama",
                "Meta_score": "77",
                "Certificate": "R"
            }
        }
        response = self.client.generic(
            method="GET",
            path=reverse('csvserv:detail', kwargs={'pk': id}),
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(
            {
                'id': id,
                'file_name': 'test_file.csv',
                'file_fields': {
                    'GenreQQQ': 'there is not such field in one or in all strings of file'
                }
            },
            response.json()
        )
