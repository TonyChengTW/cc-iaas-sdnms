import falcon

from falcon.media.validators.jsonschema import validate

from sqlalchemy.exc import IntegrityError

from cc_iaas_sdnms.db import models
from cc_iaas_sdnms.resources import BaseResource
from cc_iaas_sdnms.schemas import load_schema


class ScoresResource(BaseResource):
    def on_get(self, req, resp):
        model_list = models.UserScores.get_list(self.db.session)

        scores = [model.as_dict for model in model_list]

        resp.status = falcon.HTTP_200

        self.set_result(falcon.HTTP_200, "", {
            "scores": scores
        })

        resp.media = self.get_result()

    @validate(load_schema('scores_creation'))
    def on_post(self, req, resp):
        model = models.UserScores(
            username=req.media.get('username'),
            company=req.media.get('company'),
            score=req.media.get('score')
        )

        try:
            model.save(self.db.session)
        except IntegrityError:
            raise falcon.HTTPBadRequest(
                'Username exists',
                'Could not create user due to username already existing'
            )

        resp.status = falcon.HTTP_201
        resp.media = {
            'id': model.id
        }
