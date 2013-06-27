from gstudio.models import *
from objectapp.models import *
from django.template.defaultfilters import slugify
import inflect

pl=inflect.engine()

"""
This methods is used to create system types from the parsed data.
Adding a system type 3 fields are entered namely title, slug and sites
"""
sylist=[]

def create_system_type(stname):
    syslist=Systemtype.objects.all()

    for i in syslist:
        sylist.append(str(i.title))

    if not stname in sylist:
        slu=slugify(stname)
        st=Systemtype()
        st.title=stname
        st.slug=slu
	st.sites.add(Site.objects.get_current())
        st.save()
	sd=System.objects.get(title=stname)
	print 'The System Type created was ',sd

"""
This methods is used to create system pages from the parsed data.
Adding a System, 5 fields are entered namely title, slug, content, tags and sites
"""
def create_systems(sysname,sttype,tagname):
    systems_list=[]
    syslist=System.objects.all()
    
    for i in syslist:
	systems_list.append(i.title)

    if not sysname.decode('utf-8') in systems_list:
    	slu=slugify(sysname)
        sy=System()
        sy.title=sysname
	sy.slug=slu
        sy.content=''
        if tagname <> '':
	       	sy.tags=tagname
        sy.save()
	sys=System.objects.get(title=sysname)
	sys.systemtypes.add(Systemtype.objects.get(title=sttype))
	sys.sites.add(Site.objects.get_current())
	sys.save()
	sd=System.objects.get(title=sysname)
	print 'The System page created was ',sd

"""
This methods is used to add a system as a prior node to another system.
For this 2 system are  required as an argument
"""
def add_prior_nodes(sysname1,sysname2):
	sys1=System.objects.get(title=sysname1)
	sys2=System.objects.get(title=sysname2)
	sys1.prior_nodes.add(sys2)
	sys1.save()

"""
This methods is used to create attribute type from the parsed data.
Adding an attribute type, 5 fields are entered namely title, slug, content, status and subjecttype_id.
"""
def create_attribute_type(atname,sytype):
    att_list=[]
    atttitle=[]
    att_list=Attributetype.objects.all()

    for j in att_list:
        atttitle.append(str(j.title))

    try:
        if not atname in atttitle:
            st=Systemtype.objects.get(title=sytype)
            sid=NID.objects.get(id=st.id)
            slu=slugify(atname)
            att=Attributetype()
            att.title=atname
            att.slug=slu
            att.content=''
            att.status=2
            att.subjecttype_id=sid.id
"""	    
		print atname,sytype
#            if pl.plural(slugify(atname)) == pl.singular_noun(slugify(atname)):
#                plu=atname
#            else:
#                plu=pl.plural(atname)
#            att.plural=plu
"""
	    att.save()
	    at=Attributetype.objects.get(title=atname)
	    at.sites.add(Site.objects.get_current())
	    at.save()
	    gd=Attributetype.objects.get(title=atname)
	    print 'The Attributetype created was ',gd
    except IntegrityError:
        pass

"""
This methods is used to create attribute from the parsed data.
Adding an attribute, 5 fields are entered namely title, slug, svalue, attributetype and subject.
"""
def create_attributes(atname,sysname,attype):
    try:
	create_systems(sysname,"Wikipage","")
	st=System.objects.get(title=sysname)
        sid=NID.objects.get(id=st.id)
        at=Attributetype.objects.get(title=str(attype))
        atlist=[]
	a=Attribute.objects.all()
        for i in a:
            atlist.append(str(i))
        atvar=u'AS: the AT: %s of %s is %s' % (attype, sysname, atname)
        if not atvar in atlist:
            att=Attribute()
            slu=slugify(atname)
            att.title=atname
            att.slug=slu
            att.svalue=atname
            att.subject=sid
            try:
                att.attributetype=at
		att.save()
            except UnicodeDecodeError:
                pass
            print 'The Attribute created was : ',att
            del att
    except IntegrityError:
        pass

"""
This methods is used to create relation type from the parsed data.
Adding a relation type, 8 fields are entered namely title, slug, left_subjecttype_id, right_subjecttype_id, inverse, status, content and sites.
"""
def create_relation_type(rtname,irname,lsytype,rsytype):
    rel_list=[]
    relid_list=[]
    relnid=[]
    reltitle=[]
    rel_list=Relationtype.objects.all()
    for i in rel_list:
        relid_list.append(i.id)
    for j in relid_list:
        relnid.append(NID.objects.get(id=j))
    for k in relnid:
        reltitle.append(str(k.title))

    try:
        if not rtname in reltitle:
            ls=Systemtype.objects.get(title=lsytype)
            rs=Systemtype.objects.get(title=rsytype)
	    slu=slugify(rtname)
            rtt=Relationtype()
	    rtt.title=rtname
	    rtt.slug=slu
            if irname <> '':
                rtt.inverse=irname
            else:
                rtt.inverse=rtname
            rtt.left_subjecttype_id=ls.id
            rtt.right_subjecttype_id=rs.id
            rtt.status=2
            rtt.content=''
            rtt.save()
            rt=Relationtype.objects.get(title=rtname)
            rt.sites.add(Site.objects.get_current())
	    rt.save()
            gd=Relationtype.objects.get(title=rtname)
            print 'The Relationtype created was ',gd
	    del rtt
    except IntegrityError:
        pass

"""
This methods is used to create relation from the parsed data.
Adding a relation, 8 fields are entered namely title, slug, left_subject_id, right_subject_id, relationtype_id, left_subject_scope, right_subject_scope sand relationtype_scope.
"""
def create_relations(rtname,lsystem,rsystem):
    try:
	create_systems(lsystem,"Wikipage","")
	create_systems(rsystem,"Wikipage","")
        ls=System.objects.get(title=lsystem)
	lsid=NID.objects.get(id=ls.id)
        rs=System.objects.get(title=rsystem)
	rsid=NID.objects.get(id=rs.id)
    except System.DoesNotExist:
        pass
    try:
        rt=Relationtype.objects.get(title=rtname)
        rtid=NID.objects.get(id=rt.id)
    except Relationtype.DoesNotExist:
        pass
    try:
        slu=slugify(rtname)
        rtt=Relation()
        rtt.title=rtname
        rtt.slug=slu
        rtt.left_subject_id=lsid.id
        rtt.right_subject_id=rsid.id
        rtt.relationtype_id=rtid.id
        rtt.left_subject_scope=''
        rtt.right_subject_scope=''
        rtt.relationtype_scope=''
        rtt.save()
        print 'Relation: ',rtt
        del rtt
    except IntegrityError:
        pass

