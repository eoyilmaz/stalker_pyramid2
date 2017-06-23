=======================
Stalker Pyramid Changes
=======================

0.2.0
=====

* **New:** The system is now a complete RESTFul service.
* **Update:** Dropped the Mocker package dependency.

0.1.11
======

* **Fix:** Fixed image orientation bug. References are now displayed correctly
  if they contain an "Image Orientation" among their EXIF tags.

* **Update:** Updated the ColorBox image title field to correctly contain both
  a download link and a "open in new tab" link to the highest version of the
  related image.

0.1.10
======

* **Update:** MediaManager now replaces any Turkish characters with English
  versions of them.

* **New:** Added script for moving old style references from SPL to the
  Fileserver with new style References

* **New:** Added script to remove any unused file from SPL

* **Fix:** Fixed ``video_player.jinja2`` to center the video and maximize it to
  the whole screen,

* **Fix:** Fixed ``upload_reference`` dialog ``submit`` button to show correct
  message on file upload and video convertion.

0.1.9
=====

* **New:** References are now stored in the *Project Repository* instead of
  *Stalker Pyramid Local Storage*, allowing much bigger files to be uploaded
  (like videos). They are following the FilenameTemplate rules so the files are
  correctly placed under the Task folder (see Stalker documentation).
* **New:** Video files are now supported as both references and version
  outputs and a thumbnail is correctly created from the first, middle and last
  frames of the video. Also a version for web view (in WebM format) is saved
  under "{{Task}}/References/StalkerPyramid/ForWeb/" folder.
* **New:** Entity references are now searchable with their tags, original file
  names or entity full name.
* **New:** List Entity References page is now paginated.
* **New:** Fully implemented ``Paginator.js`` a jQuery pagination plugin.
* **Fix:** Users are not allowed to create TimeLogs for future dates.
* **Update:** Updated the SQL query for getting hierarchical Task names to a
  much better one, which allows *Depth First* or *Breadth First* sorting.
* **Fix:** Fixed performance issue in GanttChart drawing by using a pure SQL
  query in ``views.tasks.convert_to_dgrid_gantt_project_format()``.
* **Update:** Task Scheduling process UI is now much more informative. Allowing
  the user to be informed about when the process is going to end by showing a
  progress bar.
* **New:** Centralized the Task Scheduling, so that only one user at a time is
  allowed to schedule the tasks, preventing any clashes and unnecessary system
  load.
* **Update:** The calendar is now drawn way faster than before thaks to pure
  SQL queries.
* **Update:** Extended search functionality.
* **Update:** ``minute`` time unit is added to GanttChart.
* **Update:** Updated the mail content so two different emails are sent to the
  responsible and resources upon review request.
* **Update:** ``Shot.cut_in`` and ``Shot.cut_out`` attributes are now correctly
  updated (there was a bug in Stalker).

0.1.8
=====

* **New:** Updated the UI to follow changes in Stalker v0.2.5 including
  features like "Task Status Workflow", "Multiple Reviewers".

0.1.7.1
=======

* **Update:** Switched to Pillow from PIL.

0.1.7
=====

* **New:** The images on ticket comments are now copied to Stalker Storage and
  the links in the comments are replaced with proper Link instance paths. And
  the upload limit is increased to 2 MBytes per file.
* **Update:** Unified the "Review Request Dialog" over the whole site.
* **Update:** Updated the templates for "Review Request", "Ticket Update" and
  "Revision Request" mails.
* **Fix:** Fixed Ticket comment display on multiple lines when the comment is
  plain text.

0.1.6
=====

* **Update:** ``views.task.request_revision()`` will not create any new task
  anymore, it will only extend the task with the given revision timing.
* **Update:** ``views.time_log.create_time_log()`` will allow to create time
  logs for tasks with "hrev" status, and as usual it will convert the status
  to "wip" for that particular task.
* **Update:** ``views.time_log.delete_time_log()`` now doesn't allow to delete
  time logs of a completed task.
* **Update:** ``views.task.request_revision()`` now adds the revision
  description as a comment to the tickets which have the revised task in their
  links list.
* **Update:** ``views.task.request_review()`` now updates the related ticket if
  this is not the first review requested for the task.

0.1.5
=====

* **New:** Added a new status called "Ready To Start | RTS" which sits in
  between NEW and WIP. Any newly created task will have its status set to RTS
  if no dependencies has given. If there are dependencies and not all of them
  are in "Complete | CMPL" status, then the newly created tasks status will be
  NEW, otherwise its status will be RTS. And the status of all the dependent
  tasks will be updated on any review has been made to a task.
* **Fix:** Fixed ``GanttGrid.js`` where the event argument was not set for
  right arrow and down arrow key functions.
* **Fix:** A bug is fixed in ``views.entity.submit_search()`` and
  ``views.entity.list_search_result()`` views.
* **Update:** The tjp ids in the error messages of TaskJuggler are now replaced
  with correct links to the related task.

0.1.4
=====

* **New:** Added "Create" button to ``view_ticket.jinja2`` template. So it is
  now possible to create a new ticket using the dialog.
* **Fix:** Fixed "Asset", "Shot", "Sequence" menu entries under "Create" sub
  menu under "Actions" menu in ``list_tasks.jinja2`` template.
* **Fix:** Fixed "Create" button address in ``list_entity_assets.jinja2``,
  ``list_entity_shots.jinja2`` and ``list_entity_sequences.jinja2`` templates.
* **Update:** Removed schedule related fields from Task Dialog when the entity
  type is Asset, Shot or Sequence.
* **Fix:** Replaced "?came_from=" statements with proper "_query()" arguments
  in several templates.
* **New:** Link statuses are now shown in ``view_ticket.jinja2`` if the link is
  a Task derivative.
* **Fix:** Fixed a bug in the sql query in ``views.auth.get_resources()`` view.
* **New:** Added new Ticket type called "Review" and updated
  ``task.request_review()`` to use this type for newly created Review Tickets.

0.1.3
=====

* **Update:** Upgraded to `stalker v0.2.3.3`.
* **Fix:** Any TicketLog created for a Ticket is now created with UTC time.
* **Update:** When a Ticket is updated all of the previous commenters will also
  receive emails.
* **New:** Ticket status changes are also emailed to anybody related to the
  particular ticket.

0.1.2
=====

* **Update:** Upgraded to `stalker v0.2.3.2`.
* **Update:** Separated the create/update/review dialog routes for Task, Asset,
  Shot and Sequences.
* **New:** Added utc_to_local() and local_to_utc() functions to
  stalker_pyramid.views module.
* **Fix:** Added ``transaction.abort()`` statements before all return
  statements when the return value
  is a Response instance with a status integer of 500.
* **Update:** Replaced task_dialog_template.jinja2 with dialog_template.jinja2
* **New:** Added Review Task dialog.
* **Fix:** Fixed Create/Update TimeLog dialog by disabling the submit button
  when it is hit once.
* **Update:** GanttChart now shows the status of the task as the background
  color in `percent complete` column.
* **Fix:** When a review request is made for a task, the resulting Ticket is
  created in UTC time.
* **New:** Added `description` field to TimeLog create/update dialog.
* **Update:** Included `dialog_template.jinja2` in `base.jinja2` by default.
* **Update:** TimeLog dialog now only lists tasks with NEW or WIP status.
* **Update:** Replaced the queries inside
  ``stalker_pyramid.views.project.get_project_tasks_today()`` with pure sql
  queries which are ~100x faster.
* **Update:** Replaced the queries inside
  ``stalker_pyramid.views.asset.get_asset()`` with pure sql queries which are
  over ~450x faster.
* **New:** Added `stalker.less` file for the main `stalker.css` generation.
* **New:** GanttChart now displays rows in status color.
* **New:** Added ``stalker_pyramid.views.asset.get_assets_count()`` to easily
  get the asset counts.
* **New:** Parent task statuses are now updated when a review is made or a time
  log has been entered to a child task.
* **New:** Review request only can be made by one of the resources or by the
  responsible of a task.
* **New:** ``stalker_pyramid.views.task.review_task()`` will now send emails if
  the task is approved.
* **New:** Added "Request Review" button to task view.
* **Update:** Optimized the load times of the project_sidebar and user_sidebar
  menus by both using raw sql queries and changing the query and dom element
  modification orders in javascript.
* **New:** Added ``fix_task_statuses`` view to fix a particular task and its
  parent statuses according to the task/status pipeline.
* **New:** GanttChart columns can now be toggled without any problem in tree
  expansion.
* **Update:** ``stalker_pyramid.views.tasks.get_tasks()`` is now using raw sql
  query which is around ~300x faster then previous pure Python implementation.
* **New:** It is now possible to select a parent task in GanttGrid by left
  clicking from keyboard, and then collapsing the parent with a second click.

0.1.1
=====

* **Update:** Moved to Ace, a Bootstrap derived template.
* **New:** Added Resource Chart.
* **New:** Added the ability to zoom in Gantt Chart.
* **Fix:** Fixed avatar uploads in user info update page.
* **Update:** Added status and status list creation for Project, Task, Asset,
  Shot and Sequence entity types and New, Work In Progress, Pending Review,
  Has Revision and Completed to
  ``stalker_pyramid.scripts.initializedb.main()``.
* **Update:** Status colors are now coming from SimpleEntity.html_class
  attribute.

0.1.0.b4
========

* **Update:** Updating both the code and the style to Twitter Bootstrap.
* **Update:** Main Navigation Bar is updated both the code and the style to
  Twitter Bootstrap.
* **Update:** TaskJuggler error messages are now correctly displayed in the UI.
* **Update:** Updated the GanttChart theme to match the rest of the site.
* **Fix:** Task dialog is now able to create Tasks, Assets, Shots and
  Sequences.
* **Fix:** Task dialog is now working properly and it is now possible to add a
  type for the Tasks to distinguish different type of tasks like Modeling,
  Animation, Look Development, Lighting, Comp etc.
* **Fix:** It is now possible to create a child or dependent task from the
  "Create" menu in **List Tasks** view.
* **Update:** The ``chosen_field_creator()`` function now sets the field to
  ``is_updating=true`` mode before filling the data in, and back to
  ``is_updating=false`` mode after the data arrived and items are created. Also
  this is used extensively in the Task Dialog.

0.1.0.b3
========

* **Update:** Redesigned all the routes to comply with a RESTful service
  scheme.
* **New:** Leaf tasks on gantt chart now have a new functionality called
  "Request Review" which can be invoked through the context menu. It will
  create a new Ticket and assign it to the task responsible.
* **New:** Calling 'Request Review' now will send an email to the responsible
  and the logged in user.
* **Update:** It is now possible to upload multiple References.
* **Update:** Reference dialog now has a tag field.
* **Update:** "Duplicate Task Hierarchy" now confirms the action to the user
  before doing anything.
* **New:** It is now possible to create new Version files by uploading files to
  the server. Though the stalker server now needs to have a link to the file
  server.
* **Update:** Updating a StudioWide Vacation is not allowed in user vacation
  list.
* **Update:** All the DGrid table columns are now resizable.
* **Update:** GanttColumn now scrolls to the desired date so that the date will
  be in the middle of the view.
* **Update:** GanttColumn now shows the width of the days/weeks correctly.
* **New:** References are now shown in a dojox.image.LightBox dialog.
* **Fix:** Fixed **get_permissions_from_multi_dict()**, it is now skipping
  unknown access, action and class_name entries.
* **Fix:** Fixed Gantt Chart not showing completed parent tasks id column with
  a in green background.
* **New:** Added menu for Projects in Gantt Chart.
* **Fix:** The bugs after RESTful service scheme in appending user to different
   types of entity are fixed.
* **Fix:** In TimeLog UI, when updating a time log the remaining hours is
   calculated correctly by first adding the updated time log duration to the
   remaining time. Thus the ui shows the correct value after update.
* **Fix:** URL of duplicate task hierarchy method changed into Restful service
   scheme format.
* **New:** Gantt Chart is displayed in Department Views Task tab.
* **Update:** The date time format in dgrid views is turn into yyyy-mm-dd HH:MM

0.1.0.b2
========

* **New:** Stalker_Pyramid now uses a brand new implementation for the
  gantt chart which utilizes a DGrid with OnDemand capabilities. The new Gantt
  Chart is over 100x faster then the previous implementation.
* **Update:** Started to move the view designs towards a RESTFul Service style.
* **Update:** Files stored in Stalker Pyramid Local Storage (SPL Storage) are
  now reached with the 'SPL'
  (ex: http://192.168.0.64:6543/SPL/SPL/e8/cb/e8cb374b62e54165a56e216de58eede4.jpg)
  prefix instead of revealing the real path on the server.
* **New:** It is now possible to upload and query References (Link instances
  assigned as references) for Task, Asset, Shot and Sequences.
* **Update:** Adding studio vacation method is changed.Vacation that has not
    got a user is suppose to be studio vacation
* **Fix:** Minor bug is fixed in update vacation
* **Fix:** Minor bug is fixed in auth.py and time_log.py.


0.1.0.b1
========

* **Update:** The Pyramid part of Stalker is moved in to a new package (this
  one).
* **Fix:** Fixed DBSession, it is now configured with ZopeTransactionExtension
  independent of Stalkers own configuration.
* **Fix:** Fixed TimeLog update dialog timing bug. TimeTextBox values are set
  by 'set' method.
* **New:** Hierarchical names of the task are added to Task Tool Tip window.
* **New:** Hierarchical names of the task are added to Create/Update TimeLog
  dialog.
* **New:** It is now possible to duplicate a task hierarchy in gantt chart now.
* **Update:** In the summary page of Task update dialog is called based on
  task entity type.
* **New:** Update Asset MenuItem is added to right click menu on assets list
  row.
* **Update:** In Update Asset Dialog 'code' attribute is enabled to edit.
* **New:** Update Shot MenuItem is added to right click menu on shots list row.
* **Update:** In Update Shot Dialog 'code' attribute is enabled to edit.
* **New:** Update Sequence MenuItem is added to right click menu on sequences
    list row.
* **Update:** In Update Sequence Dialog 'code' attribute is enabled to edit.
* **Fix:** In Update Asset Dialog type attribute is set with value that is set
    before.
* **Fix:** Based on user permissions Studio menu is redefined.
* **New:** In List Assets Page, code of asset is added to name column.
* **New:** BID timing is added to task tooltip list.
* **Fix:** In Update Vacation Dialog predefined dates are set to dialog date
    boxes.
* **Fix:** In task dialog window submit button is disabled until resources and
    task list is loaded.
* **New:** 'Updated by' attribute is added to task summary page.
* **New:** In task create/update dialog a combo box is added to select different
    type of task entity such as Asset, Shot, Sequence. Based on the selected
    entity new properties are added to dialog form.
* **Update:** In task create/update dialog hierarchical task name order is
    reversed for easy to find.
* **New:** Remaining Time attributed is added to task tool tip window.
* **New:** In create/update timelog dialog when the alert box is appeared for
    warning about getting extra hours, user can cancel the action.
* **New:** Vacation page is created for Studio. Added create vacation dialog.
* **Fix:** Minor bug is fixed in fieldUpdater.
* **Fix:** Minor bug is fixed in create/update time log file.



* **jQueryGantt:**

  * **New:** The parent elements in gantt chart is now collapsible.
  * **Update:** Updated the CSS.
  * **New:** All the different types of elements in GridEditor (Project, Task,
    Asset, Shot, Sequence) are now drawn with different background colors.
  * **New:** Thickened the ganttLines to become the background element for
    TaskBars also they are now in the same class with the Grid elements and
    thus have the same bg color.
  * **Update:** Week zoom now shows the day number instead of the first letter
    of the day.
  * **Update:** Removed dateField.js.
  * **New:** For Tasks which are not shown because their start and end dates
    are not in range, a left or right red arrow will be drawn to show where the
    task is (on left or on right).
  * **New:** jQueryGantt now stores the collapse state of tasks in a cookie and
    upon reload of the page preserves the collapse state by not drawing
    collapsed tasks, it also helps loading the gantt chart much more quickly
    for a project with 50+ tasks.
  * **Update:** The JSON data format is changed to the following format::
    
    tasks = {
        'keys' : [key1, key2, ...., keyN]
        'data' : [
            [task1.key1, task1.key2, ....., task1.keyN],
            [task2.key1, task2.key2, ....., task2.keyN],
            ...
            [taskN.key1, taskN.key2, ....., taskN.keyN],
        ]
    }
    
    This is much more compact then the original format, because the key names
    are not repeated over and over again, causing a compression ratio of
    roughly 3.5 over the original format.
  * **Update:** Task collapse state will be preserved in different gantt chart
    views with different set of tasks from the same database.

pre 0.1.0.b1
============

* **Update:** All the date values are now returned as **UTC String** and
  stored in database as UTC datetime thus Stalker now supports Time Zones.
* **Fix:** Fixed all the dialogs with TimeTextBox inputs, where the
  date portion was reset to epoch by the widget itself, causing a change in
  Day Light Saving of the users locale and the dialog was reporting wrong
  date time values. Now in those dialogs, on submit a new date object is
  created or the DateTextBox widget value is used and the time portion of the
  Date object is updated from the TimeTextBox. This way, it is guaranteed to
  get correct date and time values.
* **Fix:** Fixed Studio create/update dialog, it is now correctly setting the
  start and end hours of a non working day.
* **New:** Studio Page is created.It has Tasks and Resources as Tabs.
* **New:** Update Studio function id added.
* **New:** Thumbnail Add function is added to several objects' Summarize Pages.
  (Task, Asset, Shot, Sequence,Department, Group). List Page is also updated
  by new thumbnail information.
* **Fix:** dgrid height attribute is updated and new div's are added for
  dgrid object.
* **Fix:** Working hours for each day is taken from database in
  Studio Update Dialog.
* **New:** List Ticket page and Create/Update Ticket dialog are created.
* **Fix:** Added logged_in_user object to user page to fix permission bug. So
  default facilities of page is define based on logged_in_user.
* **Fix:** Fixed DGrid auto height problem.
* **Fix:** GanttChart  view of Assets, Shots,Sequences or Tasks now displays
  only the children and parents of that Task derivative.
* **Update:** Task create/update dialog now displays the full hierarchy in
  parent/dependent task listings.
* **Fix:** TimeLog create/update dialog now displays the default times
  correctly when creating a new TimeLog.
* **Fix:** TimeLog create/update view callables are now checking if there
  will be any OverBookedError raised.
* **Fix:** Task create/update dialog now will not list the task itself in
  parent and dependent task lists, if the UI is called with a Task instance
  ({{task}} is not None).
* **Update:** For Asset Page and Task Page tab order is changed.
* **New:** Starts and Ends attributes are added to Task Summary Page.
* **Update:** List of Users, Departments and Groups are now sorted by using
  the name of the entity.
* **Update:** Task create/update dialog now has a new field called
  ``priority``.
* **Update:** **Task.schedule_constraint** is now filled with correct
  information when creating/updating a Task.
* **Fix:** Selected 'Status' attribute for 'Task Dialog' in 'Update' mode is
    set when dialog is open.
* **New:** Version List Page and Create/Update Dialogs are added.
* **New:** Vacation List Page and Create/Update Dialogs are added.
* **Fix:** Merge tested, and vacation adding is finished.
* **New:** Version Page is created. It has Outputs,Inputs and Children as
    Tabs.
* **New**: Added 'duration' field to TimeLog's List dgrid.
* **Fix:** Fixed the error in rendering of the **home** occurred when there is
  no user login information found in the request.
* **New:** User thumbnails now can be changed.
* **New:** Project thumbnails now can be changed.
* **New:** ``content_list_projects`` now shows the project thumbnails.
* **New:** ``content_list_users`` now shows the user thumbnails.
* **New:** ``submitForm.js`` now enables all the disabled fields of the given
  form, and disables them back again upon error.
* **Fix:** ``TagSelect.js`` will now correctly disable the child widgets if the
  ``disabled`` attribute is set to **true**.
* **New:** Added ``fields`` javascript library which are a special group of
  input fields designed to be used with Stalker.
* **New:** Added the first input field to stalker/fields, called ``tagField``.
  It is now possible to add a TagSelect field which is correctly updated by
  only two lines of code.
* **New:** Added ``get_tags()`` to stalker.views.__init__ module. Because all
  the tags now should be created with the ``tagField`` the way to retrieve tags
  is the same, so this helper function will let you retrieve tags from the
  given request instance.
* **New:** Permissions page is added to Group Page.
* **Fix:** dgrid object is declared from [Grid, Selection, Keyboard]. So it's
  possible to select a row and navigate by Keyboard.
* **New:** Permission controls are added to 'Page' and 'List' files.
* **New:** Permission controls are added to 'Dialog' and 'Summary' files.
* **Fix:** Minor bug is fixed in Update Department dialog.
* **Update:** Updated to Dojo 1.9
* **Update:** stalker.js is renamed to dialogs.js and it is now fully
  compatible with Dojo AMD.
* **Update:** Merged StatusList create and update dialogs in to one.
* **Update:** Content List - Task now checks user permissions to disable part
  of the UI.
* **Update:** Added description field to the Summarize Task view.
* **Update:** Added permission checks to several views.
* **Fix:** Fixed fieldUpdater.js to work properly with Dojo 1.9 especially for
  MultiSelect widgets.
* **Fix:** Separated the dialog and action routes for Structure.
* **Fix:** Fixed unnecessary module imports in stalker.js.
* **Fix:** Schedule button is now working properly.
* **Fix:** Fixed Image Format creation.
* **Fix:** Fixed Filename Template create dialog routine.
* **Fix:** Fixed Filename Template update dialog routine.
* **Fix:** Fixed entity_types in Filename Template creation UI.
* **Fix:** Fixed Group update dialog, the permissions were not displayed and
  the name was not updated on the server side.
* **Fix:** Fixed TaskBox CSS template
* **New:** GanttChart now displays the finished/unfinished tasks with a
  green/red 'id' column.
* **Fix:** Status color attribute converted from unicode to integer.
* **Fix:** To destroy previous open dialog, same dialog id is given for create
  and update dialogs.
* **Update:** In create/update_group dialog, to check all rows new checkboxes
  are added to head of each column.
* **Update:** ``ComboBox`` is added to TagSelect widget as a new input widget
  type.
* **Update:** Description field is added to Department dialog.
* **Fix:** ``user_create_dialog`` now shows and updates groups.
* **Fix:** Updating a project now correctly refreshes the ``project_summary``
  content pane.
* **Fix:** Separated the dialog and action routes for ImageFormat.
* **Fix:** Separated the dialog and action routes for Asset.
* **Fix:** Separated the dialog and action routes for Repository.
* **Fix:** The working hours were not correctly passed to the studio instance
  in Studio creation.
* **Fix:** "Append User Dialog" is now working properly.
* **Fix:** Links between pages is created with redirectLink function which is
  written in base.jinja2. goToLink.js is deprecated, but still there are some
  codes that uses gotolink.js, they must be changed for next update.
* **Update:** Combined ``user_create_dialog`` and ``user_update_dialog`` into
  one.
* **Update:** Logged in work times will now be visible in gantt charts as a
  green bar in the TaskBar div.
* **Update:** Department menus under 'Crew' menu are now showing the department
  users.
* **Update:** Color choosers in "Create Status Dialog" now have colors picked
  by default for BG and FG colors.
* **Update:** Replaced DataGrid objects with dgrid.
* **Update:** Added navigation bar for assets, shots, sequences.
* **Update:** Combined ``project_create_dialog`` and ``project_update_dialog``
  into one.
* **Update:** Merged the 'Crew' menu creation code in to one single
  teamMenuCreator.js, which is able to create menus for any groups and faux
  groups.
* **Update:** All DataGrid field updated with dgrid class.
* **New:** Placeholder images added for user and department.
* **New:** Added update group dialog.
* **Update:** Colors for the layouts are changed with MiamiNice PieChart's
  color.
* **New:** Added update group dialog.
* **New:** Append department and append group pages has connected to database.
* **New:** Timelog List page added.
* **New:** New placeholders added for different type of object.
* **New:** Added dialogCreator.js which helps creating a dialog without having
  a widget (Button or MenuItem) calling it and updated dialogCaller.js to use
  dialogCreator while creating a dialog.
* The Shot, Asset, Sequence detail pages under the Project Overview now opens
  inside the related tab on the Project Page.
* Updated the Create Task Dialog to reflect the TaskJuggler integration.
* Changed the license of Stalker_Pyramid from BSD-2 to LGPL 2.1. Any version
  previous to 0.2.0.a9 will be still BSD-2 and any version from and including
  0.2.0.a9 will be distributed under LGPL 2.1 license.
* TagSelect now can be filled by setting its ``value`` attribute (Ex:
  TagSelect.set('value', data))
* Fixed Projects menu in base.jinja2, the link is now updating correctly when a
  new project is added.
* Converted the ``view.py`` to a python module and put the views for each
  entity to its own python file.
* Added a new Dojo Widget called Tag to help the creation of the tags in the
  TagSelect.
* Updated java scripts to be `required` in Dojo AMD way.
* Updated setup.py to include "pyramid_jinja2"
* Added 'PlaceHolder' property for 'FilterSelect Widgets'. And 'Label' property
  is used in construction of 'PlaceHolder' property.
* Set disabled prerequisite fields, until their prerequisite is selected.
* Added **StartDate**, **EndDate** and **Duration** field to add_project page.
  **StartDate**, **EndDate** properties are now written to database.
* Project page is redesigned. SplitContainer is removed. All contents are
  displayed in TabContainer. New Contents in TabContainer are:

    * ProjectName (Disabled Field - Used for displaying projectname.)
    * Overview  (It has InlineEditable fields. Although they are not connected
      to DB.)

* Shot and Asset creation dialogs now automatically updated with the given
  Project instance info.
* User overview page is now reflection the new design.
* The WebUI form fields are now refreshed with newly added data.
* Added a new Dojo widget called TagSelect. Which is basically a widget for
  adding Tag style widgets.
* Converted the whole system to a Pyramid Web application. If the previous
  implementations investigated, it will be understood that it was only the
  database model of a Web Application.

* **jQueryGantt:**

  * **Update:** The gantt chart is now able to display much more info then
    before. There are two new modes for each of the Grid and Gantt parts of
    the Gantt Chart. Grid can be set to display *Task*\ s or *Resources* and
    the Gantt can set to display *Task*\ s or *TimeLog*\ s.
  * **Update:** Horizontal scrolling is disabled in gantt part of Gantt
    Chart. All the drawn tasks and links are now set in position with percent
    values, so they will stick and scale correctly when the split container
    resize.
  * **Update:** Any task out of range is culled in gantt chart.
  * **Update:** Added new buttons to change the range in -1/+1 month,
    -1/+1 week, -1/+1 day.
  * **Update:** Replaced the **Date.format()** (originally replaced by
    jQueryGantt **date.js**) with **date.format.js** library.
  * **Update:** Changed the background of the Grid and Gantt editors.
  * **Update:** If the displayed tasks is clipped to the current start end
    range a double red border is displayed in the clipped start or end.
  * **Update:** Context menu can now be opened in task names in grid editor.
  * **Update:** Optimized the creation of task rows.
  * **Update:** Replaced the ``input`` elements with ``div`` in the task row.
  * **New:** Holding the mouse on Task bar elements will now show a popup
    window for more info.
  * **Update:** Gantt Chart zoom levels are now fully controlled by the start
    and end date DateTextBoxes.
  * **New:** Added a new button which will center the gantt chart on today.
  * **Update:** Replaced the ``duration`` column with ``timing`` which
    correctly shows the schedule timing info of the related task.
  * **Fix:** The ``depends`` column shows the dependent task names correctly.
  * **Update:** jQueryGantt displays the owner Project of the Tasks as a
    container task.
  * **Update:** Added content link (this will be updated to support proper
    links, hardcoded links to be removed).
  * **Update:** Disabled drag and resize of TaskBar elements.
  * **Update:** Moved the resource link code to the JST template code instead
    of the Task class.
  * **Fix:** t is now possible to correctly move a TaskBar without getting in
    to an infinite loop which was freezing the browser.
  * **Update:** The timing resolution of jQueryGantt is now 1 hour.
  * **Fix:** GanttMaster.task_ids were not properly cleaned in
    GanttMaster.reset(), resulting wrong links to be created.
  * **Update:** Added a new zoom level where it is possible to see the every 1
    hour of 1 day.
  * Moving any child task will adjust the parent start and end dates so they
    fit to the children.
  * Gannt view is now communicating with Stalker correctly. The only left issue
    is the end date value is not properly shown in the gannt view.
  * Updated the jQueryGannt css's to work with Stalker and Dojo.
  * Colorized the Sunday column in suitable zoom levels. In upcoming releases
    it will use the stalker.models.studio.Studio.working_hours attribute to
    determine if the day/hour is an off day/hour.
  * Disabled editing of date fields.
  * Disabled undo/redo queue for performance test.
  * Fixed vertical overflow in gantt chart.
  * It is now possible to not to align a tasks start to its dependent tasks
    end.
  * jQueryGantt is now using the Task ids coming from Stalker instead of the
    ridiculous rowId.
  * Fixed a lot of issues related with the new data structure, it seems
    everything is working properly right now.
  * Parent Tasks displayed differently than the leaf tasks (on paar with the
    other gantt charts).
  * Gantt chart in User Detail page is now showing the parent tasks of the
    tasks of the user.
  * Now there are two different context menus for container/parent tasks and
    leaf tasks.
