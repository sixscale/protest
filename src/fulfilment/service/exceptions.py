class FulfilmentServiceException(Exception):
    pass


class FulfilmentNotFoundException(FulfilmentServiceException):
    pass


class FulfilmentCredentialsNotFoundException(FulfilmentServiceException):
    pass


class FollowingOrderNotFoundException(FulfilmentServiceException):
    pass


class LeadvertexServiceException(Exception):
    pass


class LeadvertexAPIDoesNotExist(LeadvertexServiceException):
    pass


class LeadvertexExportedStatusNotFound(LeadvertexAPIDoesNotExist):
    pass
