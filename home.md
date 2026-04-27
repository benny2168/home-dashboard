I want to create a home web app that serves as a homepage dashboard similar to Dashy, but with several additional features
- the app will be hosted in a docker container running on a Synology NAS with container manager and portainer
- the app will have local login options, as well as an option to login from users using Microsoft OAuth
- users can be grouped into organizations according to the "Department" field in their Microsoft profile
- some users can be designated as Admins either from this app's admin portal, or pulled by an admin group from Intune (all these setting scan be configured via web portal)
- the dashboard will allow users to add bookmarks to the home page via a web-page UI, each one with a link, description, icon, and the ability to open the link in sametab or new tab
- icons can be directly searched and imported from https://dashboardicons.com/, https://selfh.st/icons/, or via upload
- bookmarks can be arranged by drag/drop into customizable sections and tabs
- icon size can be customized at top level as well as user level
- admins can create sections that are available to certain organizations
- admins can theme the page with logos, light/dark mode, colors, etc
Test locally using a docker container, then we will port to Github and deploy on a synology nas running container manager/portainer


Create a task list with bugs and feature requests, and with each iteration update the list so we can keep track of what we've done

# UI Changes
- 

# Bug fixes
- for icon section, the logos search still just says "loading catalog"
- trying to upload my own logo to attach to a workspace tab, but after uploading it doesn't do anything

# Bring back features
- add the section catalog button to the dashboard, visible next to the search bar when in edit mode, that opens a modal to allows users to insert sections from the catalog.  That same modal will also allow users to look at the available themes.

# Features
- enable a "Default" workspace from the admin view for each user (this will be the workspace that is shown when the user logs in).  Also include a default default - if no default is set for a user, they will be shown the default default