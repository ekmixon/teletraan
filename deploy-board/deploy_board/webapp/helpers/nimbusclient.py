"""Helper class to connect Nimbus service"""
import logging
from decorators import singleton
from deploy_board.settings import IS_PINTEREST, NIMBUS_SERVICE_URL, NIMBUS_SERVICE_VERSION, NIMBUS_USE_EGRESS, NIMBUS_EGRESS_URL, TELETRAAN_PROJECT_URL_FORMAT
from exceptions import NotAuthorizedException, TeletraanException, FailedAuthenticationException
from urlparse import urlparse
import requests
requests.packages.urllib3.disable_warnings()

log = logging.getLogger(__name__)

@singleton
class NimbusClient(object):
    def handle_response(self, response):
        if response.status_code == 404:
            log.error(f"Resource not found. Nimbus API response - {response.content}")
            return None

        if response.status_code == 409:
            log.error(f"Resource already exists. Nimbus API response - {response.content}")
            raise TeletraanException('Resource conflict - Nimbus already has an Identifier for your proposed new stage. ')

        if 400 <= response.status_code < 600:
            log.error(f"Nimbus API Error {response.content}, {response.status_code}")
            raise TeletraanException(
                f"Teletraan failed to successfully call Nimbus. Contact your friendly Teletraan owners for assistance. Hint: {response.status_code}, {response.content}"
            )


        return response.json() if response.status_code in [200, 201] else None

    def get_one_identifier(self, name, token=None):
        service_url = NIMBUS_EGRESS_URL if NIMBUS_USE_EGRESS else NIMBUS_SERVICE_URL

        headers = {'Client-Authorization': 'client Teletraan'}
        if token:
            headers['Authorization'] = f'token {token}'

        if NIMBUS_USE_EGRESS:
            parsed_uri = urlparse(NIMBUS_SERVICE_URL)
            headers['Host'] = parsed_uri.netloc

        response = requests.get(
            f'{service_url}/api/{NIMBUS_SERVICE_VERSION}/identifiers/{name}',
            headers=headers,
        )

        return self.handle_response(response)

    def create_one_identifier(self, data, token=None):
        """
        Create a Nimbus Identifier according to the input request data.
        If the request data does not have all the information needed for creating a Nimbus identifier, this method will raise a Teletraan Exception.
        """
        requiredParams = ['projectName', 'env_name', 'stage_name']
        for param in requiredParams:
            if data.get(param) is None or len(data.get(param)) == 0:
                log.error(
                    f"Missing {param} in the request data, cannot create a Nimbus identifier"
                )

                exceptionMessage = f"Teletraan cannot create a Nimbus identifier because {param} is missing."

                if IS_PINTEREST:
                    exceptionMessage += " Contact #teletraan for assistance."
                raise TeletraanException(exceptionMessage)

        headers = {'Client-Authorization': 'client Teletraan'}
        if token:
            headers['Authorization'] = f'token {token}'

        payload = {
            'kind': 'Identifier',
            'apiVersion': 'v1',
            'platformName': 'teletraan',
            'projectName': data.get('projectName'),
        }

        cellName = None
        for property in data['propertyList']['properties']:
            if property['propertyName'] == 'cellName':
                cellName = property['propertyValue']
        if cellName is None:
            log.error("Missing cellName in the request data, cannot create a Nimbus identifier")
            exceptionMessage = "Teletraan cannot create a Nimbus identifier because cellName is missing in this env's existing identifier."
            if IS_PINTEREST:
                exceptionMessage += " Contact #teletraan for assistance."
            raise TeletraanException(exceptionMessage)

        payload['spec'] = {
            'kind': 'EnvironmentSpec',
            'apiVersion': 'v1',
            'cellName': cellName,
            'envName': data.get('env_name'),
            'stageName': data.get('stage_name')
        }

        service_url = NIMBUS_EGRESS_URL if NIMBUS_USE_EGRESS else NIMBUS_SERVICE_URL
        if NIMBUS_USE_EGRESS:
            parsed_uri = urlparse(NIMBUS_SERVICE_URL)
            headers['Host'] = parsed_uri.netloc

        response = requests.post(
            f'{service_url}/api/{NIMBUS_SERVICE_VERSION}/identifiers',
            json=payload,
            headers=headers,
        )


        return self.handle_response(response)

    def delete_one_identifier(self, name, token=None):
        headers = {'Client-Authorization': 'client Teletraan'}
        if token:
            headers['Authorization'] = f'token {token}'

        service_url = NIMBUS_EGRESS_URL if NIMBUS_USE_EGRESS else NIMBUS_SERVICE_URL
        if NIMBUS_USE_EGRESS:
            parsed_uri = urlparse(NIMBUS_SERVICE_URL)
            headers['Host'] = parsed_uri.netloc

        response = requests.delete(
            f'{service_url}/api/{NIMBUS_SERVICE_VERSION}/identifiers/{name}',
            headers=headers,
        )

        return self.handle_response(response)

    def get_one_project_console_url(self, project_name):
        return (
            TELETRAAN_PROJECT_URL_FORMAT.format(projectName=project_name)
            if TELETRAAN_PROJECT_URL_FORMAT
            else ""
        )
