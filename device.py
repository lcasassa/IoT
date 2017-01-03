from Queue import Queue
import time
import os


class RegisterClasses(object):
    class_lookup = {}

    def __init__(self):
        super(RegisterClasses, self).__init__()

    @classmethod
    def make_available(cls):
        RegisterClasses.class_lookup.update({cls.__name__: cls})

    @staticmethod
    def has_class(name):
        return name in RegisterClasses.class_lookup

    @staticmethod
    def get_class(name):
        return RegisterClasses.class_lookup[name]


class ReceiveEvents(object):
    def __init__(self):
        super(ReceiveEvents, self).__init__()
        self.receive_event_queue = Queue()

    def has_receive_event(self):
        return not self.receive_event_queue.empty()

    def get_receive_event(self):
        if self.has_receive_event():
            return self.receive_event_queue.get()
        else:
            return None

    def receive_event(self, event):
        self.receive_event_queue.put(event)


class SendEvents(object):
    def __init__(self, id=None):
        super(SendEvents, self).__init__()
        if not hasattr(self, "id") and id != None:
            self.id = id
        assert hasattr(self, "id"), "Please use BasicBlock class or call the constucter of SendEvents with a valid id argument"
        self.send_event_queue = Queue()

    def send_event(self, data):
        self.send_event_queue.put({'id': self.id, 'data': data})

    def has_send_event(self):
        return not self.send_event_queue.empty()

    def get_send_event(self):
        return self.send_event_queue.get()


class BasicBlock(RegisterClasses, ReceiveEvents, SendEvents):
    class_lookup = {}

    def __init__(self, id):
        self.id = id
        super(BasicBlock, self).__init__()

    def loop(self):
        assert False, "Please implement loop in %s" % (self.__class__.__name__)


class Input(BasicBlock):
    def __init__(self, pin, **kwargs):
        super(Input, self).__init__(**kwargs)
        self.pin = pin
        self.status = None
        self.loop()

    def loop(self):
        if os.path.isfile("input"+str(self.id)+".txt"):
            with open("input"+str(self.id)+".txt") as f:
                content = f.readlines()
                status = bool("1" in content[0])
        else:
            status = False

        if status != self.status:
            print "Input", self.id, status
            self.status = status
            self.send_event({'output': status})

        if self.has_receive_event():
            event = self.get_receive_event()
            print "Input", self.id, event
            
Input.make_available()


class Output(BasicBlock):
    def __init__(self, pin, **kwargs):
        super(Output, self).__init__(**kwargs)
        self.pin = pin
        self.loop()

    def loop(self):
        if self.has_receive_event():
            event = self.get_receive_event()
            print "Output", self.id, event

Output.make_available()


class And(BasicBlock):
    def __init__(self, **kwargs):
        super(And, self).__init__(**kwargs)
        self.inputs = {}
        self.output = None
        self.loop()

    def loop(self):
        if self.has_receive_event():
            event = self.get_receive_event()
            self.inputs.update({event['id']: event['data']['output']})

            output = True
            for b in self.inputs.values():
                if b is False:
                    output = False
                    break

            if output != self.output:
                self.output = output
                print "And", self.id, output
                self.send_event({'output': output})

And.make_available()


class MainLoop():
    def __init__(self):
        self.objects = {}
        self.connections = {}

    def create_objects(self, data, connections):
        for d in data:
            if BasicBlock.has_class(d['name']):
                print "Creating object", d['name'], d['kwargs']
                o = BasicBlock.get_class(d['name'])(**d['kwargs'])
                self.objects.update({o.id: o})
            else:
                assert False, "%s class does not exist" % d['name']

        self.connections = connections

    def loop(self):
        while True:
            for o in self.objects.values():
                o.loop()
            
            for o in self.objects.values():
                if o.has_send_event():
                    event = o.get_send_event()
                    for c in self.connections:
                        if c['from'] == event['id']:
                            if c['to'] in self.objects:
                                self.objects[c['to']].receive_event(event)
                            else:
                                assert False, "Implement communication to other devices"
            time.sleep(0.1)
                

if __name__ == "__main__":
    ml = MainLoop()
    ml.create_objects([
              {'name': 'Input', 'kwargs': {'id': 0, 'pin': 0}}, 
              {'name': 'Input', 'kwargs': {'id': 1, 'pin': 1}}, 
              {'name': 'And', 'kwargs': {'id': 2}}, 
              {'name': 'Output', 'kwargs': {'id': 3, 'pin': 2}}, 
    ], [
              {'from': 0, 'to': 2},
              {'from': 1, 'to': 2},
              {'from': 2, 'to': 3},
    ])
    ml.loop()

