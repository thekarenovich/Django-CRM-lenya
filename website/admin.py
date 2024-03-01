from django.contrib import admin
from .models import *

admin.site.register(ReagentType)
admin.site.register(ContainerType)
admin.site.register(StorageLocation)
admin.site.register(StorageChamber)
admin.site.register(Container)
admin.site.register(Reagent)
admin.site.register(OtherSolution)
admin.site.register(BufferSolution)
admin.site.register(FermentType)
admin.site.register(DrySubstanceType)
admin.site.register(PrimerType)
admin.site.register(RestrictionEnzymeType)
admin.site.register(SubstanceSolutionType)
