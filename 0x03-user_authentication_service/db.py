#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Adds a user with given email and password
        to DB and returns the newly created `User`."""
        session = self._session
        new_user = User(email=email, hashed_password=hashed_password)
        session.add(new_user)
        session.commit()
        return new_user

    def find_user_by(self, **args) -> User:
        """Searches a user with given parameters, and returns one if found.

        Raises:
            `NoResultFound` if no user is found,
            `InvalidRequestError` if `args` has an invalid user attribute."""
        user = self._session.query(User).filter_by(**args).first()
        if user is None:
            raise NoResultFound
        return user

    def update_user(self, user_id: int, **args) -> None:
        """Updates a user of given `user_id` with parameters in `args`.

        Raises:
            `ValueError` if any key in `args` is not a valid user attribute"""
        user = self.find_user_by(id=user_id)

        # check if user has all attributes to be updated
        if not all([hasattr(user, key) for key in args]):
            raise ValueError
        for key, value in args.items():     # update user attributes
            setattr(user, key, value)   # user.__dict__.update(args) DONT WORK?
        self._session.commit()
