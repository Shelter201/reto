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

#=============================================================================
class HourVotesSerializer(serializers.ModelSerializer):
    # -------------------------------------------------------------------------
    option = serializers.SerializerMethodField()
    # -------------------------------------------------------------------------
    class Meta:
        model = models.PollHourStat
        fields = ('option', 'votes')

    # -------------------------------------------------------------------------
    def get_option(self, obj):
        return obj.option.option_name

# =============================================================================
class HourStatSerializer(serializers.ModelSerializer):
    # -------------------------------------------------------------------------
    stats = serializers.SerializerMethodField()
    # -------------------------------------------------------------------------
    class Meta:
        model = models.Poll
        fields = ('name', 'stats')

    # -------------------------------------------------------------------------
    def get_option(self, obj):
        return obj.option.option_name

    # -------------------------------------------------------------------------
    def get_stats(self, obj):
        stats_by_hour = []
        hours= models.PollHourStat.objects.filter(option__poll=obj).values('vote_hour').distinct()
        for hour in hours:
            print(type(hour['vote_hour']))
            #print(hour)
            votes_records=models.PollHourStat.objects.filter(option__poll=obj, vote_hour=hour['vote_hour'])
            print(votes_records)
            votes_serializer=HourVotesSerializer(votes_records, many=True)
            stats_by_hour.append({ 'hour': hour['vote_hour'], 'stats_by_hour' : votes_serializer.data })
        stats_by_hour=sorted(stats_by_hour, key=lambda x: x['hour'])
        for x in stats_by_hour:
            x['hour']=x['hour'].strftime('%Y-%m-%d %H:%M')
        return stats_by_hour
