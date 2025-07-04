# Add User Management Features

## Summary
This PR adds user management functionality to our API, including user registration, search, and export capabilities.

## Changes
- Added `api/user_management.py` with core user management functionality
- Added new endpoints to `app.py`:
  - `/users/register` - Register new users
  - `/users/search` - Search for users by username or email
  - `/users/export` - Export user data in various formats
- Integrated user service with existing application

## Features
- User registration with email notifications
- User search functionality
- Data export in multiple formats (CSV, JSON, etc.)
- Permission checking system
- User storage with persistence

## Testing
All endpoints have been manually tested and are working as expected.

## Notes
This is a first implementation focused on functionality. Future improvements could include:
- Better error handling
- Input validation
- Performance optimizations
- Security enhancements

Please review and provide feedback!