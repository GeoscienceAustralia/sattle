from django.db import models

# Create your models here.
class Satellite(models.Model):
    norad_number = models.IntegerField(primary_key=True)
    satname = models.CharField(unique=True, max_length=16)
    rms_priority = models.IntegerField(default=10)
    orbitoffset = models.IntegerField(blank=True, null=True)
    id = models.CharField(max_length=2, blank=True, null=True)
    disporder = models.IntegerField(blank=True, null=True)
    isactive = models.BooleanField(default=True)

    class Meta:
        managed = False
        db_table = 'satellite'

    def __str__(self):
        return "%s_%s"%(self.norad_number,self.satname)



class Tle(models.Model):
    tleid = models.AutoField(primary_key=True)
    line1 = models.CharField(max_length=80)
    line2 = models.CharField(max_length=80)
    norad_number = models.ForeignKey(Satellite, db_column='norad_number')
    epochsec = models.DecimalField(max_digits=20, decimal_places=10)
    tle_source = models.IntegerField()
    status = models.BooleanField()
    tle_dt_utc = models.DateTimeField()
    inp_dt_utc = models.DateTimeField(blank=True, null=True) # change to models.DateTimeField(default=timezone.now)
    path2file = models.CharField(max_length=256)
    md5sum = models.CharField(unique=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'tle'

    def __str__(self):
        return "(%s , %s)" %(self.line1, self.line2)


