# -*- coding: utf-8 -*-
# Stalker Pyramid a Web Based Production Asset Management System
# Copyright (C) 2009-2017 Erkan Ozgur Yilmaz
#
# This file is part of Stalker Pyramid.
#
# Stalker Pyramid is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# Stalker Pyramid is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Stalker Pyramid.  If not, see <http://www.gnu.org/licenses/>.

import datetime
from pyramid.view import view_config

from stalker import Status, Budget, BudgetEntry, Good
from stalker.db.session import DBSession

import transaction

from webob import Response
from stalker_pyramid2.views import (logger,
                                    PermissionChecker,
                                    local_to_utc, StdErrToHTMLConverter)



# @view_config(
#     route_name='create_budget'
# )
# def create_budget(request):
#     """runs when creating a budget
#     """
#
#     logged_in_user = get_logged_in_user(request)
#     utc_now = local_to_utc(datetime.datetime.now())
#
#     name = request.params.get('name')
#     description = request.params.get('description')
#
#     type_name = request.params.get('type_name', None)
#     budget_type = query_type('Budget', type_name)
#
#     project_id = request.params.get('project_id', None)
#     project = Project.query.filter(Project.id == project_id).first()
#
#     if not name:
#         return Response('Please supply a name', 500)
#
#     if not description:
#         return Response('Please supply a description', 500)
#
#     # if not status:
#     #     return Response('There is no status with code: %s' % status_id, 500)
#
#     if not project:
#         return Response('There is no project with id: %s' % project_id, 500)
#
#     budget = Budget(
#         project=project,
#         name=name,
#         type=budget_type,
#         description=description,
#         created_by=logged_in_user,
#         date_created=utc_now,
#         date_updated=utc_now
#     )
#     DBSession.add(budget)
#
#     return Response('Budget Created successfully')


@view_config(
    route_name='update_budget'
)
def update_budget(request):
    """runs when updating a budget
    """

    logged_in_user = get_logged_in_user(request)
    utc_now = local_to_utc(datetime.datetime.now())

    budget_id = request.matchdict.get('id', -1)
    budget = Budget.query.filter(Budget.id == budget_id).first()

    if not budget:
        transaction.abort()
        return Response('No budget with id : %s' % budget_id, 500)

    name = request.params.get('name')
    description = request.params.get('description')

    status_id = request.params.get('status_id')
    status = Status.query.filter(Status.id == status_id).first()

    if not name:
        return Response('Please supply a name', 500)

    if not description:
        return Response('Please supply a description', 500)

    if not status:
        return Response('There is no status with code: %s' % status.code, 500)

    budget.name = name
    budget.description = description
    budget.status = status
    budget.date_updated = utc_now
    budget.updated_by = logged_in_user

    request.session.flash('success: Successfully updated budget')
    return Response('Successfully updated budget')


def get_budgets(request):
    """returns budgets with the given id
    """

    project_id = request.matchdict.get('id')
    logger.debug('get_budgets is working for the project which id is: %s' % project_id)

    status_code = request.params.get('status_code', None)
    status = Status.query.filter(Status.code == status_code).first()

    sql_query = """
        select
            "Budgets".id,
            "Budget_SimpleEntities".name,
            "Created_By_SimpleEntities".created_by_id,
            "Created_By_SimpleEntities".name,
            "Type_SimpleEntities".name,
            (extract(epoch from "Budget_SimpleEntities".date_created::timestamp at time zone 'UTC') * 1000)::bigint as date_created

        from "Budgets"
        join "SimpleEntities" as "Budget_SimpleEntities" on "Budget_SimpleEntities".id = "Budgets".id
        join "SimpleEntities" as "Created_By_SimpleEntities" on "Created_By_SimpleEntities".id = "Budget_SimpleEntities".created_by_id
        left outer join "SimpleEntities" as "Type_SimpleEntities" on "Type_SimpleEntities".id = "Budget_SimpleEntities".type_id
        join "Projects" on "Projects".id = "Budgets".project_id

        where "Projects".id = %(project_id)s %(additional_condition)s
    """

    additional_condition = ''
    if status:
        additional_condition = 'and "Budgets_Statuses".id=%s' % status.id

    budgets = []

    sql_query = sql_query % {'project_id': project_id, 'additional_condition':additional_condition}

    result = DBSession.connection().execute(sql_query)
    update_budget_permission = \
        PermissionChecker(request)('Update_Budget')

    for r in result.fetchall():
        budget = {
            'id': r[0],
            'name': r[1],
            'created_by_id': r[2],
            'created_by_name': r[3],
            'item_view_link': '/budgets/%s/view' % r[0],
            'type_name': r[4],
            'date_created': r[5]
        }
        if update_budget_permission:
            budget['item_update_link'] = \
                '/budgets/%s/update/dialog' % budget['id']
            budget['item_remove_link'] =\
                '/budgets/%s/delete/dialog?came_from=%s' % (
                    budget['id'],
                    request.current_route_path()
                )

        budgets.append(budget)

    resp = Response(
        json_body=budgets
    )

    return resp


def get_budgets_count(request):
    """missing docstring
    """
    project_id = request.matchdict.get('id')
    logger.debug('get_budgets_count is working for the project which id is %s' % project_id)

    sql_query = """
        select count(1) from (
            select
                "Budgets".id
            from "Budgets"
            join "Projects" on "Projects".id = "Budgets".project_id

            where "Projects".id = %(project_id)s
        ) as data
    """
    sql_query = sql_query % {'project_id': project_id}

    from sqlalchemy import text  # to be able to use "%" sign use this function
    result = DBSession.connection().execute(text(sql_query))

    return result.fetchone()[0]


# @view_config(
#     route_name='save_budget_calendar'
# )
# def save_budget_calendar(request):
#     """saves the data that is created on budget calendar as a string and
#     """
#     logger.debug('***save_budget_calendar method starts ***')
#     logged_in_user = get_logged_in_user(request)
#     utc_now = local_to_utc(datetime.datetime.now())
#
#     budget_id = request.matchdict.get('id', -1)
#     budget = Budget.query.filter(Budget.id == budget_id).first()
#
#     if not budget:
#         transaction.abort()
#         return Response('No budget with id : %s' % budget_id, 500)
#
#     budgetentries_data = get_multi_string(request, 'budgetentries_data')
#
#     if not budgetentries_data:
#         return Response('No task is defined on calendar for budget id %s' % budget_id, 500)
#
#     budget.generic_text = '&'.join(budgetentries_data)
#     logger.debug('***budget.generic_text %s ***'% budget.generic_text)
#     for budget_entry in budget.entries:
#         if budget_entry.generic_text == 'Calendar':
#             # delete_budgetentry_action(budget_entry)
#             logger.debug('***delete *** %s ' % budget_entry.name)
#             DBSession.delete(budget_entry)
#
#     for budgetentry_data in budgetentries_data:
#         logger.debug('budgetentry_data: %s' % budgetentry_data)
#
#         id, text, gid, sdate, duration, resources = budgetentry_data.split('-')
#         good_id = gid.split('_')[1]
#         good = Good.query.filter_by(id=good_id).first()
#         logger.debug('good: %s' % good)
#         if not good:
#             transaction.abort()
#             return Response('Please supply a good', 500)
#
#         amount = int(duration.split('_')[1])*int(resources.split('_')[1])
#
#         if good.unit == 'HOUR':
#             amount *= 9
#         if amount or amount > 0:
#             create_budgetentry_action(budget,
#                                       good,
#                                       amount,
#                                       good.cost * amount,
#                                       ' ',
#                                       'Calendar',
#                                       logged_in_user,
#                                       utc_now)
#
#     return Response('Budget Calendar Saved Succesfully')


# @view_config(
#     route_name='edit_budgetentry'
# )
# def edit_budgetentry(request):
#     """edits the budgetentry with data from request
#     """
#     logger.debug('***edit budgetentry method starts ***')
#     oper = request.params.get('oper', None)
#
#     if oper == 'edit':
#         e_id = request.params.get('id')
#         logger.debug('***edit_budgetentry good: %s ***' % e_id)
#
#         entity = Entity.query.filter_by(id=e_id).first()
#
#         if not entity:
#             transaction.abort()
#             return Response('There is no entry with id %s' % e_id, 500)
#
#         if entity.entity_type == 'Good':
#             logger.debug('***create budgetentry method starts ***')
#             return create_budgetentry(request)
#         elif entity.entity_type == 'BudgetEntry':
#             logger.debug('***update budgetentry method starts ***')
#             return update_budgetentry(request)
#         else:
#             transaction.abort()
#             return Response('There is no budgetentry or good with id %s' % e_id, 500)
#
#     elif oper == 'del':
#         logger.debug('***delete budgetentry method starts ***')
#         return delete_budgetentry(request)


# @view_config(
#     route_name='create_budgetentry'
# )
# def create_budgetentry(request):
#     """runs when creating a budget
#     """
#     logger.debug('***create_budgetentry method starts ***')
#     logged_in_user = get_logged_in_user(request)
#     utc_now = local_to_utc(datetime.datetime.now())
#
#     good_id = request.params.get('good_id', None)
#     if not good_id:
#         good_id = request.params.get('id', None)
#
#     logger.debug('good_id %s ' % good_id)
#     good = Good.query.filter_by(id=good_id).first()
#     if not good:
#         transaction.abort()
#         return Response('Please supply a good', 500)
#
#     budget_id = request.params.get('budget_id', None)
#     budget = Budget.query.filter(Budget.id == budget_id).first()
#     if not budget:
#         transaction.abort()
#         return Response('There is no budget with id %s' % budget_id, 500)
#
#     amount = request.params.get('amount')
#     price = request.params.get('price')
#     description = request.params.get('description', '')
#
#     if not amount or amount == '0':
#         transaction.abort()
#         return Response('Please supply the amount', 500)
#
#     if price == '0':
#         price = good.cost * int(amount)
#
#     if amount and price:
#         # data that's generate from good's data
#
#         create_budgetentry_action(budget,
#                                   good,
#                                   int(amount),
#                                   int(price),
#                                   description,
#                                   'Producer',
#                                   logged_in_user,
#                                   utc_now)
#
#     else:
#         transaction.abort()
#         return Response('There are missing parameters', 500)
#
#     return Response('BudgetEntry Created successfully')


# def create_budgetentry_action(budget, good, amount, price, description, gText, logged_in_user, utc_now):
#     """create_budgetentry_action
#     """
#     logger.debug('good_id: %s' % good.id)
#     logger.debug('amount: %s' % amount)
#
#     for budget_entry in budget.entries:
#         if budget_entry.name == good.name:
#             logger.debug('Adds budget_entry amount %s ***'% budget_entry.amount)
#             budget_entry.amount += amount
#             budget_entry.price += price
#             return
#
#     cost = good.cost
#     msrp = good.msrp
#     realize_total = msrp
#     unit = good.unit
#     entry_type = query_type('BudgetEntries', good.price_lists[0].name)
#
#     budget_entry = BudgetEntry(
#         budget=budget,
#         good=good,
#         name=good.name,
#         type=entry_type,
#         amount=amount,
#         cost=cost,
#         msrp=msrp,
#         price=price,
#         realize_total=realize_total,
#         unit=unit,
#         description=description,
#         created_by=logged_in_user,
#         date_created=utc_now,
#         date_updated=utc_now,
#         generic_text=gText
#     )
#     DBSession.add(budget_entry)
#     return


@view_config(
    route_name='update_budgetentry'
)
def update_budgetentry(request):
    """updates the budgetentry with data from request
    """

    logger.debug('***update_budgetentry method starts ***')
    logged_in_user = get_logged_in_user(request)
    utc_now = local_to_utc(datetime.datetime.now())

    budgetentry_id = request.params.get('id')
    budgetentry = BudgetEntry.query.filter_by(id=budgetentry_id).first()

    good = Good.query.filter(Good.name == budgetentry.name).first()
    # user supply this data
    amount = request.params.get('amount', None)
    price = request.params.get('price', None)
    if not price:
        transaction.abort()
        return Response('Please supply price', 500)
    price = int(price)
    description = request.params.get('note', '')

    if budgetentry.generic_text == 'Calendar':
        budgetentry.price = price
        budgetentry.description = description
        budgetentry.date_updated = utc_now
        budgetentry.updated_by = logged_in_user
    else:
        if not amount or amount == '0':
            transaction.abort()
            return Response('Please supply the amount', 500)

        amount = int(amount)
        budgetentry.amount = amount
        budgetentry.cost = good.cost
        budgetentry.msrp = good.msrp
        budgetentry.good = good
        # budgetentry.realized_total = good.msrp
        budgetentry.price = price if price != '0' else good.cost*amount
        budgetentry.description = description
        budgetentry.date_updated = utc_now
        budgetentry.updated_by = logged_in_user
        budgetentry.generic_text = 'Producer'

    request.session.flash(
                'success:updated %s budgetentry!' % budgetentry.name
            )
    return Response('successfully updated %s budgetentry!' % budgetentry.name)


@view_config(
    route_name='delete_budgetentry'
)
def delete_budgetentry(request):
    """deletes the budgetentry
    """

    budgetentry_id = request.params.get('id')
    budgetentry = BudgetEntry.query.filter_by(id=budgetentry_id).first()

    if not budgetentry:
        transaction.abort()
        return Response('There is no budgetentry with id: %s' % budgetentry_id, 500)

    if budgetentry.type.name == 'Calendar':
        transaction.abort()
        return Response('You can not delete CalenderBasedEntry', 500)

    delete_budgetentry_action(budgetentry)


def delete_budgetentry_action(budgetentry):

    logger.debug('delete_budgetentry_action %s' % budgetentry.name)
    budgetentry_name = budgetentry.name
    try:
        DBSession.delete(budgetentry)
        transaction.commit()
    except Exception as e:
        transaction.abort()
        c = StdErrToHTMLConverter(e)
        transaction.abort()
        # return Response(c.html(), 500)
    # return Response('Successfully deleted good with name %s' % budgetentry_name)


@view_config(
    route_name='get_budget_entries',
    renderer='json'
)
def get_budget_entries(request):
    """returns budgets with the given id
    """

    budget_id = request.matchdict.get('id')
    logger.debug('get_budget_entries is working for the project which id is: %s' % budget_id)

    sql_query = """
        select
           "BudgetEntries_SimpleEntities".id,
           "BudgetEntries_SimpleEntities".name,
           "Types_SimpleEntities".name as type_name,
           "BudgetEntries".amount,
           "BudgetEntries".cost,
           "BudgetEntries".msrp,
           "BudgetEntries".price,
           "BudgetEntries".realized_total,
           "BudgetEntries".unit,
           "BudgetEntries_SimpleEntities".description,
           "BudgetEntries_SimpleEntities".generic_text
        from "BudgetEntries"
        join "SimpleEntities" as "BudgetEntries_SimpleEntities" on "BudgetEntries_SimpleEntities".id = "BudgetEntries".id
        join "SimpleEntities" as "Types_SimpleEntities" on "Types_SimpleEntities".id = "BudgetEntries_SimpleEntities".type_id
        join "Budgets" on "Budgets".id = "BudgetEntries".budget_id
        where "Budgets".id = %(budget_id)s
    """

    sql_query = sql_query % {'budget_id': budget_id}

    result = DBSession.connection().execute(sql_query)
    entries = [
        {
            'id': r[0],
            'name': r[1],
            'type': r[2],
            'amount': r[3],
            'cost': r[4],
            'msrp': r[5],
            'price': r[6],
            'realized_total': r[7],
            'unit': r[8],
            'note': r[9],
            'addition_type': r[10]
        }
        for r in result.fetchall()
    ]

    resp = Response(
        json_body=entries
    )

    return resp


# @view_config(
#     route_name='change_budget_type'
# )
# def change_budget_type(request):
#
#     logged_in_user = get_logged_in_user(request)
#     utc_now = local_to_utc(datetime.datetime.now())
#
#     budget_id = request.matchdict.get('id')
#     budget = Budget.query.filter_by(id=budget_id).first()
#
#     if not budget:
#         transaction.abort()
#         return Response('There is no budget with id %s' % budget_id, 500)
#
#     type_name = request.matchdict.get('type_name')
#     type = query_type('Budget', type_name)
#
#     budget.type = type
#     budget.updated_by = logged_in_user
#     budget.date_updated = utc_now
#
#     request.session.flash('success: Budget type is changed successfully')
#     return Response('Budget type is changed successfully')


# @view_config(
#     route_name='duplicate_budget'
# )
# def duplicate_budget(request):
#
#     logged_in_user = get_logged_in_user(request)
#     utc_now = local_to_utc(datetime.datetime.now())
#
#     budget_id = request.matchdict.get('id')
#     budget = Budget.query.filter_by(id=budget_id).first()
#
#     if not budget:
#         transaction.abort()
#         return Response('There is no budget with id %s' % budget_id, 500)
#
#     name = request.params.get('dup_budget_name')
#     description = request.params.get('dup_budget_description')
#
#
#     budget_type = query_type('Budget', 'Planning')
#     project = budget.project
#
#     if not name:
#         return Response('Please supply a name', 500)
#
#     if not description:
#         return Response('Please supply a description', 500)
#
#     new_budget = Budget(
#         project=project,
#         name=name,
#         type=budget_type,
#         description=description,
#         created_by=logged_in_user,
#         date_created=utc_now,
#         date_updated=utc_now,
#         generic_text=budget.generic_text
#     )
#     DBSession.add(budget)
#     for budget_entry in budget.entries:
#         new_budget_entry = BudgetEntry(
#                 budget=new_budget,
#                 good= budget_entry.good,
#                 name=budget_entry.name,
#                 type=budget_entry.type,
#                 amount=budget_entry.amount,
#                 cost=budget_entry.cost,
#                 msrp=budget_entry.msrp,
#                 price=budget_entry.price,
#                 unit=budget_entry.unit,
#                 description=budget_entry.description,
#                 created_by=logged_in_user,
#                 date_created=utc_now,
#                 date_updated=utc_now,
#                 generic_text=budget_entry.generic_text
#             )
#         DBSession.add(new_budget_entry)
#
#
#     request.session.flash('success: Budget is duplicated successfully')
#     return Response('Budget is duplicated successfully')
