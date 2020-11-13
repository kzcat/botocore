from botocore.stub import Stubber
from tests import BaseSessionTest


class TestSagemaker(BaseSessionTest):
    def setUp(self):
        super(TestSagemaker, self).setUp()
        self.region = 'us-west-2'
        self.client = self.session.create_client(
            'sagemaker', self.region)
        self.stubber = Stubber(self.client)
        self.stubber.activate()
        self.hook_calls = []

    def _hook(self, **kwargs):
        self.hook_calls.append(kwargs['event_name'])

    def tearDown(self):
        self.stubber.deactivate()

    def test_event_with_old_prefix(self):
        self.client.meta.events.register(
            'provide-client-params.sagemaker.ListEndpoints',
            self._hook
        )
        self.stubber.add_response('list_endpoints', {'Endpoints': []})
        self.client.list_endpoints()
        assert self.hook_calls == [
            'provide-client-params.sagemaker.ListEndpoints'
        ]

    def test_event_with_new_prefix(self):
        self.client.meta.events.register(
            'provide-client-params.api.sagemaker.ListEndpoints',
            self._hook
        )
        self.stubber.add_response('list_endpoints', {'Endpoints': []})
        self.client.list_endpoints()
        assert self.hook_calls == [
            'provide-client-params.sagemaker.ListEndpoints'
        ]