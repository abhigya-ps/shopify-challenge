import unittest
import demo
import helper

class TestDemo(unittest.TestCase):
    def test_add(self):
        result = demo.add(10, 5)
        self.assertEqual(result, 15)

    def test_add2(self):
        result = demo.add(100, 200)
        self.assertEqual(result, 300)

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


if __name__ == "__main__":
    unittest.main()