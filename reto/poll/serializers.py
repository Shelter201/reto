from rest_framework import serializers

from poll import models


# =============================================================================
class StatSerializer(serializers.ModelSerializer):
    # -------------------------------------------------------------------------
    option = serializers.SerializerMethodField()
    # -------------------------------------------------------------------------
    class Meta:
        model = models.PollStat
        fields = ('option', 'votes')

    # -------------------------------------------------------------------------
    def get_option(self, obj):
        return obj.option.option_name
