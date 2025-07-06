from flask_restful import Resource
from flask import request
from sqlalchemy import select, or_, desc, asc
from sqlalchemy.sql import func
from db import engine, spots_table, categories_table

class Spots(Resource):
    def get(self):
        # 取得 QueryString 參數
        keyword = request.args.get('keyword', '').strip()
        category_id = request.args.get('category_id')
        page = int(request.args.get('page', 1))
        per_page = max(3, min(int(request.args.get('per_page', 9)), 45))
        sort_by = request.args.get('sort_by', 'SpotId')
        sort_order = request.args.get('sort_order', 'asc').lower()

        # 驗證排序欄位
        valid_sort_fields = ['SpotId', 'SpotTitle', 'CategoryId']
        if sort_by not in valid_sort_fields:
            sort_by = 'SpotId'
        if sort_order not in ['asc', 'desc']:
            sort_order = 'asc'

        # 排序欄位動態選擇
        sort_column = spots_table.c.get(sort_by)
        sort_expr = asc(sort_column) if sort_order == 'asc' else desc(sort_column)

        # 基礎查詢條件
        conditions = []
        if keyword:
            conditions.append(
                or_(
                    spots_table.c.SpotTitle.contains(keyword),
                    spots_table.c.SpotDescription.contains(keyword)
                )
            )
        if category_id and category_id != "0":
            conditions.append(spots_table.c.CategoryId == category_id)
       

        # 計算總筆數與頁數
        count_stmt = select(func.count()).select_from(spots_table).where(*conditions)
        with engine.connect() as conn:
            total_count = conn.execute(count_stmt).scalar()
            total_pages = (total_count + per_page - 1) // per_page  # 無條件進位

            # 實際查詢資料
            stmt = (
                select(spots_table)
                .where(*conditions)
                .order_by(sort_expr)
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            result = conn.execute(stmt)
            data = [dict(row._mapping) for row in result]

            return {
                'total_pages': total_pages,
                'data': data
            }, 200

class SpotCategoryStats(Resource):
    def get(self):
        stmt = (
            select(
                categories_table.c.CategoryName,
                func.count(spots_table.c.SpotId).label("count")
            )
            .select_from(
                spots_table.join(
                    categories_table,
                    spots_table.c.CategoryId == categories_table.c.CategoryId
                )
            )
            .group_by(categories_table.c.CategoryName)
            .order_by(categories_table.c.CategoryId)
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            data = [
                {"category": row.CategoryName, "count": row.count}
                for row in result
            ]

        return {"data": data}, 200

class SpotsByDistrict(Resource):
    def get(self):       
        keyword = request.args.get('district')  

        stmt = (
            select(
                spots_table.c.SpotTitle,
                spots_table.c.Longitude,
                spots_table.c.Latitude
            )
            .where(spots_table.c.Address.contains(keyword))
        )

        with engine.connect() as conn:
            result = conn.execute(stmt)
            data = [
                {
                    "title": row.SpotTitle,
                    "lng": float(row.Longitude),
                    "lat": float(row.Latitude)
                }
                for row in result
                if row.Longitude and row.Latitude
            ]
        return data, 200
        # return {"spots": data}, 200
