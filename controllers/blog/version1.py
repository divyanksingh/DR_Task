from flask import Blueprint, request
from controllers.blog.base import BaseBlog
from application.extensions import db
from rest.restfull import register_url
from models.blog import Blog
import json
from datetime import datetime


blog_version1 = Blueprint('blog_version1', __name__)


class Version1(object):
    VERSION = 1
    BLUEPRINT = blog_version1


class BlogCRUD(Version1, BaseBlog):

    def get(self, id):
        if id is None:
            per_page_count = 2
            max_cache_size = 5
            params = request.args
            refresh = params.get('refresh', False)
            max_id = params.get('max_id')
            since_id = params.get('since_id')
            last_updated = params.get('last_updated')
                
            if refresh:
                if not (max_id and since_id and last_updated):
                    """
                    For cache refresh all three parameters are required
                    """
                    return (422, {"message": "max_id, since_id and last_updated are mandatory"}, {})
                    
                last_updated = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')
                rewrite = False
                latest_id = db.session.query(db.func.max(Blog.id)).scalar()
                if latest_id > int(since_id) + max_cache_size:
                    """
                        Rewrite cache as blog with since_id is older than maximum size of the cache
                    """ 
                    rewrite = True
                    next_page = db.session.query(Blog).order_by(db.desc(Blog.id)).\
                    limit(per_page_count).all()
                elif latest_id > int(max_id) + max_cache_size:
                    """
                        Refresh cache with all blogs having id greater than latest_id - max_cache_size
                        and last_updated greater than the latest update time received from client
                    """ 
                    next_page = db.session.query(Blog).filter(
                        db.and_(
                            Blog.id >= latest_id - max_cache_size,
                            Blog.last_updated > last_updated
                            )
                        ).order_by(db.desc(Blog.id)).all()
                else:
                    """
                        Refresh cache with all blogs having id greater than max_id and last_updated
                        greater than the latest update time received from client
                    """ 
                    next_page = db.session.query(Blog).filter(
                            db.and_(
                                Blog.id >= max_id,
                                Blog.last_updated > last_updated
                            )
                        ).order_by(db.desc(Blog.id)).all()
            else:
                if max_id:
                    """
                        Fetch next page of blogs after last blog id equal to max_id
                    """ 
                    next_page = db.session.query(Blog).filter(Blog.id < max_id).\
                    order_by(db.desc(Blog.id)).limit(per_page_count).all()
                else:
                    """
                        Fetch blogs when the cache is empty
                    """
                    next_page = db.session.query(Blog).order_by(db.desc(Blog.id)).\
                    limit(per_page_count).all()

            blog_list = []
            for item in next_page:
                    blog_list.append({
                        "blog_id": item.id,
                        "title": item.title,
                        "description": item.description,
                        "last_updated": item.last_updated.strftime("%Y-%m-%d %H:%M:%S"),
                        "deleted": item.deleted
                        })
            return (200, {"blog_list": blog_list}, {})
        
        else:
            blog = db.session.query(Blog).get(id).first()
            if not blog:
                return (404, {"message": "Blog not found"}, {})    
            return (200, {"title": blog.title, "blog_id": blog.id, "description": blog.description,\
            "last_updated": blog.last_updated.strftime("%Y-%m-%d %H:%M:%S"), "deleted": blog.deleted}, {})
        

    def post(self):
        data = json.loads(request.data.decode('utf-8'))
        title = data.get('title', None)
        if not title:
            return (422, {"message": "Title is mandatory"}, {})
        description = data.get('description')
        blog = Blog()
        blog.title = title
        blog.description = description
        db.session.add(blog)
        db.session.commit()
        return (201, {"blog_id": blog.id}, {})

    def delete(self, id):
        blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return (404, {"message": "Blog not found"}, {}) 
        blog.last_updated = datetime.utcnow()
        blog.deleted = True
        db.session.add(blog)
        db.session.commit()
        return (200, {}, {})


    def put(self, id):
        data = json.loads(request.data.decode('utf-8'))
        title = data.get('title', None)
        description = data.get('description', None)
        blog = db.session.query(Blog).filter(Blog.id == blog_id).first()
        if not blog:
            return (404, {"message": "Blog not found"}, {}) 
        if title:
            blog.title = title
        if description:
            blog.description = description
        blog.last_updated = datetime.utcnow()
        db.session.add(blog)
        db.session.commit()
        return (200, {"blog_id": blog.id, "title": blog.title, "description": blog.description}, {})



register_url(Version1)