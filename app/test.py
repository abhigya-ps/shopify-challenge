import unittest
import helper

class TestHelper(unittest.TestCase):
    def test_prev_url_checker(self):
        url_a = "http://127.0.0.1:5000/favorites/"
        self.assertEqual(helper.prev_url_checker(url_a), 'favorites')

        url_b = "http://127.0.0.1:5000/tags/school/"
        self.assertEqual(helper.prev_url_checker(url_b), ('tags', 'school'))

        url_c = "http://127.0.0.1:5000/"
        self.assertEqual(helper.prev_url_checker(url_c), 'home')
    
    def test_file_format(self):
        self.assertFalse(helper.file_format('photo.docx'))
        self.assertTrue(helper.file_format('photo.png'))

    def test_no_file_name(self):
        self.assertTrue(helper.no_file_name('.jpeg'))
        self.assertFalse(helper.no_file_name('picture.jpeg'))
    
    def test_error_type(self):
        title_error = '(sqlite3.IntegrityError) UNIQUE constraint failed: saved_images.title \n [SQL: INSERT INTO saved_images (title, category, filename, favorite) VALUES (?, ?, ?, ?)]'
        self.assertEqual(helper.error_type(title_error), 'use a different title for your image')

        filename_error = '(sqlite3.IntegrityError) UNIQUE constraint failed: saved_images.filename \n [SQL: INSERT INTO saved_images (title, category, filename, favorite) VALUES (?, ?, ?, ?)]'
        self.assertEqual(helper.error_type(filename_error), 'image already exists')
        
        other_error = '(sqlite3.IntegrityError) UNIQUE constraint failed'
        self.assertEqual(helper.error_type(other_error), 'something went wrong with the upload')
    
    # def test_get_images(self):
    #     all_images = ['uploads/cousin-ritas-home.jpg',
    #                 'uploads/garlic-naan.jpg',
    #                 'uploads/group-study.jpg',
    #                 'uploads/work-from-home.jpg',
    #                 'uploads/geneva-day-trip.webp',
    #                 'uploads/jens-painting.jpg',
    #                 'uploads/chon-at-audiotree.jpg']
    #     self.assertEqual(helper.get_images(), all_images)

if __name__ == "__main__":
    unittest.main()