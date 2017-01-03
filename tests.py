import device
from nose.tools import assert_equal
from nose.tools import assert_not_equal
from nose.tools import assert_raises
from nose.tools import raises


class TestReceiveEvents(object):
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
        r = device.ReceiveEvents()
        assert_equal(r.has_receive_event(), False)
        assert_equal(r.get_receive_event(), None)
        event = ["abs", {1:2, 3:4}]
        r.receive_event(event)
        assert_equal(r.has_receive_event(), True)
        assert_equal(r.get_receive_event(), event)


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
        assert_equal(device.RegisterClasses.has_class("A"), False)
        assert_equal(device.RegisterClasses.has_class("B"), False)
        assert_equal(device.RegisterClasses.has_class("C"), False)
        a.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_equal(device.RegisterClasses.has_class("B"), False)
        assert_equal(device.RegisterClasses.has_class("C"), False)
        b.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_equal(device.RegisterClasses.has_class("B"), True)
        assert_equal(device.RegisterClasses.has_class("C"), False)
        c.make_available()
        assert_equal(device.RegisterClasses.has_class("A"), True)
        assert_equal(device.RegisterClasses.has_class("B"), True)
        assert_equal(device.RegisterClasses.has_class("C"), True)

        assert_equal(device.RegisterClasses.get_class("A").__name__, A.__name__)
        assert_equal(device.RegisterClasses.get_class("B").__name__, B.__name__)
        assert_equal(device.RegisterClasses.get_class("C").__name__, C.__name__)

if __name__ == '__main__':
    import nose
    nose.runmodule()