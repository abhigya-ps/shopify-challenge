import unittest
import helper

class TestHelper(unittest.TestCase):
    def test_prevUrlChecker(self):
        url_a = "http://127.0.0.1:5000/favorites/"
        self.assertEqual(helper.prevUrlChecker(url_a), 'favorites')

        url_b = "http://127.0.0.1:5000/tags/school/"
        self.assertEqual(helper.prevUrlChecker(url_b), ('tags', 'school'))

        url_c = "http://127.0.0.1:5000/"
        self.assertEqual(helper.prevUrlChecker(url_c), 'home')
    
    def test_fileFormat(self):
        self.assertFalse(helper.fileFormat('photo.docx'))
        self.assertTrue(helper.fileFormat('photo.png'))

    def test_noFileName(self):
        self.assertTrue(helper.noFileName('.jpeg'))
        self.assertFalse(helper.noFileName('picture.jpeg'))
    
    def test_errorType(self):
        titleError = '(sqlite3.IntegrityError) UNIQUE constraint failed: saved_images.title \n [SQL: INSERT INTO saved_images (title, category, filename, favorite) VALUES (?, ?, ?, ?)]'
        self.assertEqual(helper.errorType(titleError), 'use a different title for your image')

        filenameError = '(sqlite3.IntegrityError) UNIQUE constraint failed: saved_images.filename \n [SQL: INSERT INTO saved_images (title, category, filename, favorite) VALUES (?, ?, ?, ?)]'
        self.assertEqual(helper.errorType(filenameError), 'image already exists')
        
        otherError = '(sqlite3.IntegrityError) UNIQUE constraint failed'
        self.assertEqual(helper.errorType(otherError), 'something went wrong with the upload')
    
    # def test_getImages(self):
    #     allImages = ['uploads/cousin-ritas-home.jpg',
    #                 'uploads/garlic-naan.jpg',
    #                 'uploads/group-study.jpg',
    #                 'uploads/work-from-home.jpg',
    #                 'uploads/geneva-day-trip.webp',
    #                 'uploads/jens-painting.jpg',
    #                 'uploads/chon-at-audiotree.jpg']
    #     self.assertEqual(helper.getImages(), allImages)

if __name__ == "__main__":
    unittest.main()