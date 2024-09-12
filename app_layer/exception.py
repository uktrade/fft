#  Pixel Code
#  Email: haresh@pixelcode.uk
#
#  Copyright (c) 2024.
#
#  All rights reserved.
#
#  No part of this code may be used or reproduced in any manner whatsoever without the prior written consent of the author.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
#  BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
#  SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
#  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
#  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
#  OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#  For permission requests, write to the author, at the email address above.

"""
exception.py contains custom exception classes for the service.

The ServiceException class is a custom exception class for the service.

Attributes
----------
message (str)
    The message of the exception

Methods
----------
append_message(message) -> ServiceException
    Append a message to the exception
to_dict() -> dict
    Convert the exception to a dictionary

Custom exceptions are defined for:
    - Empty or None Value
    - Unknown Value
    - Value Exists
    - Key Not Found
"""
__version__: str = '0.0.1'


class ServiceException(Exception):
    """
    A custom exception class for service

    Attributes
    ----------
    message (str)
        The message of the exception

    Methods
    ----------
    append_message(message) -> ServiceException
        Append a message to the exception
    to_dict() -> dict
        Convert the exception to a dictionary

    """

    message = None

    def __init__(self, message: str):
        """
        Constructs all the necessary attributes for the ServiceException object.

        Parameters
        ----------
        message : str
            The message of the exception
        """
        self.message = message
        super().__init__(self.message)

    @classmethod
    def append_message(cls, message) -> 'ServiceException':
        """
        Append a message to the exception

        Parameters
        ----------
        message : str
            The message to append to the exception

        Returns
        ----------
        ServiceException
            The exception with the appended message
        """
        cls.message = message if cls.message is None else cls.message + f" - {message}"
        return cls(cls.message)

    def to_dict(self) -> dict:
        """
        Convert the exception to a dictionary

        Returns
        ----------
        dict
            The exception as a dictionary
        """
        return {
            "message": self.message
        }


# Custom exception for empty or none value not permitted
class EmptyOrNoneValueException(ServiceException):
    def __init__(self, message="empty or none value not permitted"):
        super().__init__(message)


# Custom exception for unknown and/or not recognised value
class UnknownValueException(ServiceException):
    def __init__(self, message="unknown and/or not recognised value"):
        super().__init__(message)


# Custom exception for value already exists
class ValueExistsException(ServiceException):
    def __init__(self, message="value already exists"):
        super().__init__(message)


# Custom exception for key not found
class KeyNotFoundException(ServiceException):
    def __init__(self, message="key not found"):
        super().__init__(message)
