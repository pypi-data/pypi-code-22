import json
import requests
import requests.exceptions
import requests.packages.urllib3

from . import __version__ as version


class DefectDojoAPI(object):
    """An API wrapper for DefectDojo."""

    def __init__(self, host, api_key, user, api_version='v1', verify_ssl=True, timeout=60, proxies=None, user_agent=None, cert=None, debug=False):
        """Initialize a DefectDojo API instance.

        :param host: The URL for the DefectDojo server. (e.g., http://localhost:8000/DefectDojo/)
        :param api_key: The API key generated on the DefectDojo API key page.
        :param user: The user associated with the API key.
        :param api_version: API version to call, the default is v1.
        :param verify_ssl: Specify if API requests will verify the host's SSL certificate, defaults to true.
        :param timeout: HTTP timeout in seconds, default is 30.
        :param proxies: Proxy for API requests.
        :param user_agent: HTTP user agent string, default is "DefectDojo_api/[version]".
        :param cert: You can also specify a local cert to use as client side certificate, as a single file (containing
        the private key and the certificate) or as a tuple of both file's path
        :param debug: Prints requests and responses, useful for debugging.

        """

        self.host = host + '/api/' + api_version + '/'
        self.api_key = api_key
        self.user = user
        self.api_version = api_version
        self.verify_ssl = verify_ssl
        self.proxies = proxies
        self.timeout = timeout

        if not user_agent:
            self.user_agent = 'DefectDojo_api/' + version
        else:
            self.user_agent = user_agent

        self.cert = cert
        self.debug = debug  # Prints request and response information.

        if not self.verify_ssl:
            requests.packages.urllib3.disable_warnings()  # Disabling SSL warning messages if verification is disabled.

    ###### Helper Functions ######
    def get_user_uri(self, user_id):
        """Returns the DefectDojo API URI for a user.

        :param user_id: Id of the user

        """

        return "/api/" + self.api_version + "/users/" + str(user_id) + "/"

    def get_engagement_uri(self, engagement_id):
        """Returns the DefectDojo API URI for an engagement.

        :param engagement_id: Id of the engagement

        """
        return "/api/" + self.api_version + "/engagements/" + str(engagement_id) + "/"

    def get_product_uri(self, product_id):
        """Returns the DefectDojo API URI for a product.

        :param product_id: Id of the product

        """
        return "/api/" + self.api_version + "/products/" + str(product_id) + "/"

    def get_test_uri(self, test_id):
        """Returns the DefectDojo API URI for a test.

        :param test_id: Id of the test

        """
        return "/api/" + self.api_version + "/tests/" + str(test_id) + "/"

    def version_url(self):
        """Returns the DefectDojo API version.

        """
        return self.api_version

    def get_id_from_url(self, url):
        """Returns the ID from the DefectDojo API.

        :param url: URL returned by the API

        """
        url = url.split('/')
        return url[len(url)-2]


    ###### User API #######
    def list_users(self, username=None, limit=20):
        """Retrieves all the users.

        :param username: Search by username.
        :param limit: Number of records to return.

        """
        params  = {}
        if limit:
            params['limit'] = limit

        if username:
            params['username'] = username

        return self._request('GET', 'users/', params)

    def get_user(self, user_id):
        """Retrieves a user using the given user id.

        :param user_id: User identification.

        """
        return self._request('GET', 'users/' + str(user_id) + '/')

    ###### Engagements API #######
    def list_engagements(self, status=None, product_in=None, name_contains=None,limit=20):
        """Retrieves all the engagements.

        :param product_in: List of product ids (1,2).
        :param name_contains: Engagement name
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if product_in:
            params['product__in'] = product_in

        if status:
            params['status'] = status

        if name_contains:
            params['name_contains'] = name_contains

        return self._request('GET', 'engagements/', params)

    def get_engagement(self, engagement_id):
        """Retrieves an engagement using the given engagement id.

        :param engagement_id: Engagement identification.

        """
        return self._request('GET', 'engagements/' + str(engagement_id) + '/')

    def create_engagement(self, name, product_id, lead_id, status, target_start, target_end, active='True',
        pen_test='False', check_list='False', threat_model='False', risk_path="", test_strategy="", progress="",
        done_testing='False'):
        """Creates an engagement with the given properties.

        :param name: Engagement name.
        :param product_id: Product key id..
        :param lead_id: Testing lead from the user table.
        :param status: Engagement Status: In Progress, On Hold, Completed.
        :param target_start: Engagement start date.
        :param target_end: Engagement end date.
        :param active: Active
        :param pen_test: Pen test for engagement.
        :param check_list: Check list for engagement.
        :param threat_model: Thread Model for engagement.
        :param risk_path: risk_path
        :param test_strategy: Test Strategy URLs
        :param progress: Engagement progresss measured in percent.

        """

        data = {
            'name': name,
            'product': self.get_product_uri(product_id),
            'lead': self.get_user_uri(lead_id),
            'status': status,
            'target_start': target_start,
            'target_end': target_end,
            'active': active,
            'pen_test': pen_test,
            'check_list': check_list,
            'threat_model': threat_model,
            'risk_path': risk_path,
            'test_strategy': test_strategy,
            'progress': progress,
            'done_testing': done_testing
        }

        return self._request('POST', 'engagements/', data=data)

    def set_engagement(self, id, name=None, product_id=None, lead_id=None, status=None, target_start=None,
        target_end=None, active=None, pen_test=None, check_list=None, threat_model=None, risk_path=None,
        test_strategy=None, progress=None, done_testing=None):

        """Updates an engagement with the given properties.

        :param id: Engagement id.
        :param name: Engagement name.
        :param product_id: Product key id..
        :param lead_id: Testing lead from the user table.
        :param status: Engagement Status: In Progress, On Hold, Completed.
        :param target_start: Engagement start date.
        :param target_end: Engagement end date.
        :param active: Active
        :param pen_test: Pen test for engagement.
        :param check_list: Check list for engagement.
        :param threat_model: Thread Model for engagement.
        :param risk_path: risk_path
        :param test_strategy: Test Strategy URLs
        :param progress: Engagement progresss measured in percent.

        """

        data = {}

        if name:
            data['name'] = name

        if product_id:
            data['product'] = self.get_product_uri(product_id)

        if lead_id:
            data['lead'] = self.get_user_uri(user_id)

        if status:
            data['status'] = status

        if target_start:
            data['target_start'] = target_start

        if target_end:
            data['target_end'] = target_end

        if active:
            data['active'] = active

        if pen_test:
            data['pen_test'] = pen_test

        if check_list:
            data['check_list'] = check_list

        if threat_model:
            data['threat_model'] = threat_model

        if risk_path:
            data['risk_path'] = risk_path

        if test_strategy:
            data['test_strategy'] = test_strategy

        if progress:
            data['progress'] = progress

        if done_testing:
            data['done_testing'] = done_testing

        return self._request('PUT', 'engagements/' + str(id) + '/', data=data)

    ###### Product API #######
    def list_products(self, name=None, name_contains=None, limit=20):
        """Retrieves all the products.

        :param name: Search by product name.
        :param name_contains: Search by product name.
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name'] = name

        if name_contains:
            params['name__icontains'] = name_contains

        return self._request('GET', 'products/', params)

    def get_product(self, product_id):
        """Retrieves a product using the given product id.

        :param product_id: Product identification.

        """
        return self._request('GET', 'products/' + str(product_id) + '/')

    def create_product(self, name, description, prod_type):
        """Creates a product with the given properties.

        :param name: Product name.
        :param description: Product key id..
        :param prod_type: Product type.

        """

        data = {
            'name': name,
            'description': description,
            'prod_type': prod_type
        }

        return self._request('POST', 'products/', data=data)

    def set_product(self, product_id, name=None, description=None, prod_type=None):
        """Updates a product with the given properties.

        :param product_id: Product ID
        :param name: Product name.
        :param description: Product key id..
        :param prod_type: Product type.

        """

        data = {}

        if name:
            data['name'] = name

        if description:
            data['description'] = description

        if prod_type:
            data['prod_type'] = prod_type

        return self._request('PUT', 'products/' + str(product_id) + '/', data=data)


    ###### Test API #######
    def list_tests(self, name=None, engagement_in=None, limit=20):
        """Retrieves all the tests.

        :param name_contains: Search by product name.
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if engagement_in:
            params['engagement__in'] = engagement_in

        return self._request('GET', 'tests/', params)

    def get_test(self, test_id):
        """Retrieves a test using the given test id.

        :param test_id: Test identification.

        """
        return self._request('GET', 'tests/' + str(test_id) + '/')

    def create_test(self, engagement_id, test_type, environment, target_start, target_end, percent_complete=None):
        """Creates a product with the given properties.

        :param engagement_id: Engagement id.
        :param test_type: Test type key id.
        :param target_start: Test start date.
        :param target_end: Test end date.
        :param percent_complete: Percentage until test completion.

        """

        data = {
            'engagement': self.get_engagement_uri(engagement_id),
            'test_type': test_type,
            'environment': environment,
            'target_start': target_start,
            'target_end': target_end,
            'percent_complete': percent_complete
        }

        return self._request('POST', 'tests/', data=data)

    def set_test(self, test_id, engagement_id=None, test_type=None, environment=None,
        target_start=None, target_end=None, percent_complete=None):
        """Creates a product with the given properties.

        :param engagement_id: Engagement id.
        :param test_type: Test type key id.
        :param target_start: Test start date.
        :param target_end: Test end date.
        :param percent_complete: Percentage until test completion.

        """

        data = {}

        if engagement_id:
            data['engagement'] = self.get_engagement_uri(engagement_id)

        if test_type:
            data['test_type'] = test_type

        if environment:
            data['environment'] = environment

        if target_start:
            data['target_start'] = target_start

        if target_end:
            data['target_end'] = target_end

        if percent_complete:
            data['percent_complete'] = percent_complete

        return self._request('PUT', 'tests/' + str(test_id) + '/', data=data)

    ###### Findings API #######
    def list_findings(self, active=None, duplicate=None, mitigated=None, severity=None, verified=None, severity_lt=None,
        severity_gt=None, severity_contains=None, title_contains=None, url_contains=None, date_lt=None,
        date_gt=None, date=None, product_id_in=None, engagement_id_in=None, test_id_in=None, build=None, limit=20):

        """Returns filtered list of findings.

        :param active: Finding is active: (true or false)
        :param duplicate: Duplicate finding (true or false)
        :param mitigated: Mitigated finding (true or false)
        :param severity: Severity: Low, Medium, High and Critical.
        :param verified: Finding verified.
        :param severity_lt: Severity less than Low, Medium, High and Critical.
        :param severity_gt: Severity greater than Low, Medium, High and Critical.
        :param severity_contains: Severity contains: (Medium, Critical)
        :param title_contains: Filter by title containing the keyword.
        :param url_contains: Filter by URL containing the keyword.
        :param date_lt: Date less than.
        :param date_gt: Date greater than.
        :param date: Return findings for a particular date.
        :param product_id_in: Product id(s) associated with a finding. (1,2 or 1)
        :param engagement_id_in: Engagement id(s) associated with a finding. (1,2 or 1)
        :param test_in: Test id(s) associated with a finding. (1,2 or 1)
        :param build_id: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if active:
            params['active'] = active

        if duplicate:
            params['duplicate'] = duplicate

        if mitigated:
            params['mitigated'] = mitigated

        if severity:
            params['severity__in'] = severity

        if verified:
            params['verified'] = verified

        if severity_lt:
            params['severity__lt'] = severity_lt

        if severity_gt:
            params['severity__gt'] = severity_gt

        if severity_contains:
            params['severity__contains'] = severity_contains

        if title_contains:
            params['title__contains'] = title_contains

        if url_contains:
            params['url__contains'] = url_contains

        if date_lt:
            params['date__lt'] = date_lt

        if date_gt:
            params['date__gt'] = date_gt

        if date:
            params['date'] = date

        if engagement_id_in:
            params['engagement__id__in'] = engagement_id_in

        if product_id_in:
            params['product__id__in'] = product_id_in

        if test_id_in:
            params['test__id__in'] = test_id_in

        if build:
            params['build_id__contains'] = build

        return self._request('GET', 'findings/', params)

    def get_finding(self, finding_id):
        """
        Retrieves a finding using the given finding id.
        :param finding_id: Finding identification.
        """
        return self._request('GET', 'findings/' + str(finding_id) + '/')

    def create_finding(self, title, description, severity, cwe, date, product_id, engagement_id, test_id, user_id,
        impact, active, verified, mitigation, references=None, build=None):

        """Creates a finding with the given properties.

        :param title: Finding title
        :param description: Finding detailed description.
        :param severity: Finding severity: Low, Medium, High and Critical
        :param cwe: CWE (int)
        :param date: Discovered Date.
        :param product_id: Product finding should be associated with.
        :param engagement_id: Engagement finding should be associated with.
        :param test_id: Test finding should be associated with.
        :param user_id: Reporter of finding.
        :param impact: Detailed impact of finding.
        :param active: Finding active and reported on.
        :param verified: Finding has been verified.
        :param mitigation: Steps to mitigate the finding.
        :param references: Details on finding.
        :param build: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).
        """

        data = {
            'title': title,
            'description': description,
            'severity': severity,
            'cwe': cwe,
            'date': date,
            'product': self.get_product_uri(product_id),
            'engagement': self.get_engagement_uri(engagement_id),
            'test': self.get_test_uri(test_id),
            'reporter': self.get_user_uri(user_id),
            'impact': impact,
            'active': active,
            'verified': verified,
            'mitigation': mitigation,
            'references': references,
            'build_id' : build
        }

        return self._request('POST', 'findings/', data=data)

    def set_finding(self, finding_id, product_id, engagement_id, test_id, title=None, description=None, severity=None,
        cwe=None, date=None, user_id=None, impact=None, active=None, verified=None,
        mitigation=None, references=None):

        """Updates a finding with the given properties.

        :param title: Finding title
        :param description: Finding detailed description.
        :param severity: Finding severity: Low, Medium, High and Critical
        :param cwe: CWE (int)
        :param date: Discovered Date.
        :param product_id: Product finding should be associated with.
        :param engagement_id: Engagement finding should be associated with.
        :param test_id: Test finding should be associated with.
        :param user_id: Reporter of finding.
        :param impact: Detailed impact of finding.
        :param active: Finding active and reported on.
        :param verified: Finding has been verified.
        :param mitigation: Steps to mitigate the finding.
        :param references: Details on finding.
        :param build: User specified build id relating to the build number from the build server. (Jenkins, Travis etc.).

        """

        data = {}

        if title:
            data['title'] = title

        if description:
            data['description'] = description

        if severity:
            data['severity'] = severity

        if cwe:
            data['cwe'] = cwe

        if date:
            data['date'] = date

        if product_id:
            data['product'] = self.get_product_uri(product_id)

        if engagement_id:
            data['engagement'] = self.get_engagement_uri(engagement_id)

        if test_id:
            data['test'] = self.get_test_uri(test_id)

        if user_id:
            data['reporter'] = self.get_user_uri(user_id)

        if impact:
            data['impact'] = impact

        if active:
            data['active'] = active

        if verified:
            data['verified'] = verified

        if mitigation:
            data['mitigation'] = mitigation

        if references:
            data['references'] = references

        if build:
            data['build_id'] = build

        return self._request('PUT', 'findings/' + str(finding_id) + '/', data=data)

    ##### Upload API #####

    def upload_scan(self, engagement_id, scan_type, file, active, scan_date, tags=None, build=None):
        """Uploads and processes a scan file.

        :param application_id: Application identifier.
        :param file_path: Path to the scan file to be uploaded.

        """
        if tags is None:
            tags = ''

        if build is None:
            build = ''

        data = {
            'file': open(file, 'rb'),
            'engagement': ('', self.get_engagement_uri(engagement_id)),
            'scan_type': ('', scan_type),
            'active': ('', active),
            'scan_date': ('', scan_date),
            'tags': ('', tags),
            'build_id': ('', build)
        }

        return self._request(
            'POST', 'importscan/',
            files=data
        )

    ##### Credential API #####

    def list_credentials(self, name=None, username=None, limit=20):
        """Retrieves all the globally configured credentials.

        :param name_contains: Search by credential name.
        :param username: Search by username
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        if username:
            params['username__contains'] = username

        return self._request('GET', 'credentials/', params)

    def get_credential(self, cred_id, limit=20):
        """
        Retrieves a credential using the given credential id.
        :param credential_id: Credential identification.
        """
        return self._request('GET', 'credentials/' + str(cred_id) + '/')

    ##### Credential Mapping API #####

    def list_credential_mappings(self, name=None, product_id_in=None, engagement_id_in=None, test_id_in=None, finding_id_in=None, limit=20):
        """Retrieves mapped credentials.

        :param name_contains: Search by credential name.
        :param username: Search by username
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name'] = name

        if product_id_in:
            params['product__id__in'] = product_id_in

        if engagement_id_in:
            params['engagement__id__in'] = engagement_id_in

        if test_id_in:
            params['test__id__in'] = test_id_in

        if finding_id_in:
            params['finding__id__in'] = finding_id_in

        return self._request('GET', 'credential_mappings/', params)

    def get_credential_mapping(self, cred_mapping_id, limit=20):
        """
        Retrieves a credential using the given credential id.
        :param cred_mapping_id: Credential identification.
        """
        return self._request('GET', 'credential_mappings/' + str(cred_mapping_id) + '/')

    ##### Container API #####

    def list_containers(self, name=None, container_type=None, limit=20):
        """Retrieves all the globally configured credentials.

        :param name_contains: Search by credential name.
        :param username: Search by username
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        if container_type:
            params['container_type__contains'] = container_type

        return self._request('GET', 'container/', params)

    def get_container(self, container_id, limit=20):
        """
        Retrieves a finding using the given container id.
        :param container_id: Container identification.
        """
        return self._request('GET', 'container/' + str(container_id) + '/')

    ###### Tool API #######

    def list_tool_types(self, name=None, limit=20):
        """Retrieves all the tool types.

        :param name_contains: Search by tool type name.
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        return self._request('GET', 'tool_types/', params)

    def list_tools(self, name=None, tool_type_id=None, limit=20):
        """Retrieves all the tools.

        :param name_contains: Search by tool name.
        :param tool_type_id: Search by tool type id
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        if tool_type_id:
            params['tool_type__id'] = tool_type_id

        return self._request('GET', 'tools/', params)

    def list_tool_products(self, name=None, tool_configuration_id=None, limit=20):
        """Retrieves all the tools.

        :param name_contains: Search by tool name.
        :param tool_type_id: Search by tool type id
        :param limit: Number of records to return.

        """

        params  = {}
        if limit:
            params['limit'] = limit

        if name:
            params['name__contains'] = name

        if tool_configuration_id:
            params['tool_configuration__id'] = tool_configuration_id

        return self._request('GET', 'tool_configs/', params)

    # Utility

    @staticmethod
    def _build_list_params(param_name, key, values):
        """Builds a list of POST parameters from a list or single value."""
        params = {}
        if hasattr(values, '__iter__'):
            index = 0
            for value in values:
                params[str(param_name) + '[' + str(index) + '].' + str(key)] = str(value)
                index += 1
        else:
            params[str(param_name) + '[0].' + str(key)] = str(values)
        return params

    def _request(self, method, url, params=None, data=None, files=None):
        """Common handler for all HTTP requests."""
        if not params:
            params = {}

        if data:
            data = json.dumps(data)

        headers = {
            'User-Agent': self.user_agent,
            'Authorization' : "ApiKey " + self.user + ":" + self.api_key
        }

        if not files:
            headers['Accept'] = 'application/json'
            headers['Content-Type'] = 'application/json'

        if self.proxies:
            proxies=self.proxies
        else:
            proxies = {}

        try:
            if self.debug:
                print(method + ' ' + url)
                print(params)

            response = requests.request(method=method, url=self.host + url, params=params, data=data, files=files, headers=headers,
                                        timeout=self.timeout, verify=self.verify_ssl, cert=self.cert, proxies=proxies)

            if self.debug:
                print(response.status_code)
                print(response.text)

            try:
                if response.status_code == 201: #Created new object
                    object_id = response.headers["Location"].split('/')
                    key_id = object_id[-2]
                    try:
                        data = int(key_id)
                    except:
                        data = response.json()

                    return DefectDojoResponse(message="Upload complete", data=data, success=True)
                elif response.status_code == 204: #Object updates
                    return DefectDojoResponse(message="Object updated.", success=True)
                elif response.status_code == 400: #Object not created
                    return DefectDojoResponse(message="Error occured in API.", success=False, data=response.text)
                elif response.status_code == 404: #Object not created
                    return DefectDojoResponse(message="Object id does not exist.", success=False, data=response.text)
                elif response.status_code == 401:
                    return DefectDojoResponse(message="Unauthorized.", success=False, data=response.text)
                elif response.status_code == 414:
                    return DefectDojoResponse(message="Request-URI Too Large.", success=False)
                elif response.status_code == 500:
                    return DefectDojoResponse(message="An error 500 occured in the API.", success=False, data=response.text)
                else:
                    data = response.json()
                    return DefectDojoResponse(message="Success", data=data, success=True, response_code=response.status_code)
            except ValueError:
                return DefectDojoResponse(message='JSON response could not be decoded.', success=False, data=response.text)
        except requests.exceptions.SSLError:
            return DefectDojoResponse(message='An SSL error occurred.', success=False)
        except requests.exceptions.ConnectionError:
            return DefectDojoResponse(message='A connection error occurred.', success=False)
        except requests.exceptions.Timeout:
            return DefectDojoResponse(message='The request timed out after ' + str(self.timeout) + ' seconds.',
                                     success=False)
        except requests.exceptions.RequestException:
            return DefectDojoResponse(message='There was an error while handling the request.', success=False)


class DefectDojoResponse(object):
    """
    Container for all DefectDojo API responses, even errors.

    """

    def __init__(self, message, success, data=None, response_code=-1):
        self.message = message
        self.data = data
        self.success = success
        self.response_code = response_code

    def __str__(self):
        if self.data:
            return str(self.data)
        else:
            return self.message

    def id(self):
        if self.response_code == 400: #Bad Request
            raise ValueError('Object not created:' + json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': ')))
        return int(self.data)

    def count(self):
        return self.data["meta"]["total_count"]

    def data_json(self, pretty=False):
        """Returns the data as a valid JSON string."""
        if pretty:
            return json.dumps(self.data, sort_keys=True, indent=4, separators=(',', ': '))
        else:
            return json.dumps(self.data)
