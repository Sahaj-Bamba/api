from django.db import *
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def get_value(col, table, cond, val, db):
    sql = "select %s from %s where %s like '%s'" % (col, table, cond, val)
    row = query(db, sql)
    if len(row) > 0:
        if col == '*':
            return row[0]
        return row[0][col]
    return ''


def get_val_multi_cond(col, table, cond, val, db):
    """
     for multi columns or multi condition use list to pass value
    """
    sql = "select "
    no_of_col = len(col)
    curr_no = 0

    for curr_col in col:
        if curr_no == no_of_col - 1:
            sql = sql + " " + str(curr_col)
        else:
            sql = sql + " " + str(curr_col) + ","
        curr_no = curr_no + 1

    sql = sql + "  from " + table + " where "

    curr_no = 0
    no_of_cond = len(cond)
    for curr_cond in cond:
        if curr_no == no_of_cond - 1:
            sql = sql + " " + str(curr_cond) + " like " + "\'" + str(val[curr_no]) + "\'"
        else:
            sql = sql + " " + str(curr_cond) + " like " + "\'" + str(val[curr_no]) + "\' and "
        curr_no = curr_no + 1
    row = query(db, sql)
    if row:
        return row[0]
    return ''


def query(db, sql):
    cursor = connections[str(db)].cursor()
    print(sql)
    try:
        cursor.execute(sql)
        row = dictfetchall(cursor)
        return row
    except DatabaseError as e:
        sqlobj = sqlerror.objects.create(error=e, sql=sql, db=db)
        sqlobj.save()
        raise ValueError('Error !!')


def udi_query(db, sql):
    cursor = connections[str(db)].cursor()
    try:
        cursor.execute(sql)
    except DatabaseError as e:
        sqlobj = sqlerror.objects.create(error=e, sql=sql, db=db)
        sqlobj.save()
        raise ValueError('Error !!')