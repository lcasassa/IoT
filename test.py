import device
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestRegisterClasses(object):
    @classmethod
    def setup_class(klass):
        """This method is run once for each class before any tests are run"""

    @classmethod
    def teardown_class(klass):
        """This method is run once for each class _after_ all tests are run"""

    def setUp(self):
        """This method is run once before _each_ test method is executed"""

    def teardown(self):
        """This method is run once after _each_ test method is executed"""

    def test_init(self):
        class A(device.RegisterClasses):
            pass
        class B(device.RegisterClasses):
            pass
        class C(device.RegisterClasses):
            pass
        a = A()
        b = B()
        c = C()
        assert_not_equal(device.RegisterClasses.has_class("A"), True)
        assert_not_equal(device.RegisterClasses.has_class("B"), True)
        assert_not_equal(device.RegisterClasses.has_class("C"), True)
        a.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_not_equal(device.RegisterClasses.has_class("B"), True)
        assert_not_equal(device.RegisterClasses.has_class("C"), True)
        b.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_equal(device.RegisterClasses.has_class("B"), True)
        assert_not_equal(device.RegisterClasses.has_class("C"), True)
        c.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_equal(device.RegisterClasses.has_class("B"), True)
        assert_equal(device.RegisterClasses.has_class("C"), True)

        assert_equal(device.RegisterClasses.get_class("A").__name__, A.__name__)
        assert_equal(device.RegisterClasses.get_class("B").__name__, B.__name__)
        assert_equal(device.RegisterClasses.get_class("C").__name__, C.__name__)
