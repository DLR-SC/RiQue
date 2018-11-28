import json 
import py2neo # library used to comunicate with database
from py2neo import Graph
import spacy


graph = Graph("http://localhost:7474", auth=("neo4j", "123456"))

# Convert Json file to graphs

# In order to convert json source file to graph database, 
# we use neo4j database which uses cypher query language. 
# To visualize the graph, login to  http://localhost:7474

def convertJsonToNeo4j():

	# load json file
	with open('./data/rte.json') as data_file:
	    json_ = json.load(data_file)

	# write cypher query
	query = '''

	WITH {json} as document
	UNWIND document.bundles AS p
	MERGE(rce: project {name:toLower(document.name), 
	    className: toLower(document.eClass), timeStamp: document.modelTimestamp})
	    

	MERGE (b: bundles {name:toLower(p.name), className:toLower(p.eClass)}) SET b.symbolicName=toLower(p.symbolicName)
	MERGE(rce)-[:has_bundles]->(b)

	    // bundle > imports 
	    FOREACH (imp IN p.imports | 
	       MERGE(im: PackagesImports {name:toLower(imp.ref)}) SET im.FullName=toLower(imp.ref)

	     MERGE(b)-[:imports]->(im))

	    // bundle > exports
	    FOREACH (exp IN p.exports | 
	        MERGE(ex: PackagesExports {name:toLower(exp.ref)} ) SET ex.FullName=toLower(exp.ref) 
	        MERGE(b)-[:exports]->(ex))
	        
	    // bundle > packages
	    FOREACH (pkg IN p.packages | 

	        MERGE(pk: packages {name:toLower(pkg.ref)} ) SET pk.FullName=toLower(pkg.ref)
	        MERGE(b)-[:uses_pkgs]->(pk))
	    
	    // Iterate through bundle > components
	    
	    FOREACH (comp IN p.components | 

	        MERGE (b)-[:uses_components]-> (c: Components {name:toLower(comp.name)} ) 
	            SET c.className=toLower(comp.eClass), 
	            c.implementation = toLower(comp.implementation.ref),
	            c.bundle = toLower(comp.bundle.ref)
	        
	        // Iterate through bundle > components > provided services
	        
	        FOREACH (service in comp.providedServices| 
	             MERGE(c)-[:uses_services]->(sr: ComponentServices 
	                                     {name: toLower(service.ref) }) )
	        
	    )
	    // Iterate through bundle > packageFragment
	    
	    FOREACH (pkgfrag IN p.packageFragments |
	        MERGE(b)-[:Pkg_fragment]->(fragment: PackageFragments {name:toLower(pkgfrag.eClass)}) 
	                SET fragment.className = toLower(pkgfrag.eClass)
	        MERGE(fragment)-[:Pack_By_Frag]->(pack: FragPackages {name:toLower(pkgfrag.package.ref)})
	        MERGE(fragment)-[:Bundle_By_Frag]->
	                (bund: FragBundle {name:toLower(pkgfrag.bundle.ref) })

	    // Iterate through bundle > packageFragment > compilation units
	    
	    FOREACH (cmp IN pkgfrag.compilationUnits | 
	        MERGE(fragment)-[:compiled_By]->(u: compilationUnit{name:toLower(cmp.name)}) 
	                    SET u.className = toLower(cmp.eClass),
	                    u.Loc = cmp.LOC

	        // Iterate through bundle > packageFragment > compilation units > packageFragment
	        MERGE(u)-[:compiledUnits_pkgFragment]->
	        (CPkFrag: compiledUF 
	                {name:toLower(cmp.packageFragment.ref)}) 

	        // bundle > packageFragment > compilationUnits -> topLevelType

	        MERGE(u)-[:compiledUnits_topLevelType]->
	        (CPtpLevelType: compiledTopLevelType {name:toLower(cmp.topLevelType.name)}) 
	                    SET  CPtpLevelType.className = toLower(cmp.topLevelType.eClass),
	        CPtpLevelType.visibility = toLower(cmp.topLevelType.visibility), 
	        CPtpLevelType.qualifiedName = toLower(cmp.topLevelType.qualifiedName)

	        // bundle > packageFragment > compilationUnits -> topLevelType > compilationUnits

	        MERGE(CPtpLevelType) -[:topLevelType_compilationUnit]->
	        (topLevel_cUnit: Units {name: toLower(cmp.topLevelType.compilationUnit.ref) } ) 
	        SET topLevel_cUnit.ref = toLower(cmp.topLevelType.compilationUnit.ref)


	        // Inside topLevelType > references

	        FOREACH (refer IN cmp.topLevelType.references |
	            MERGE(CPtpLevelType)-[:topLevelType_reference]->
	                    (referTL: References {name:tolower(refer.ref) })
	            SET referTL.ref = tolower(refer.ref)
	        )
	        
	        // Inside bundle > packageFragment > compilationUnits -> topLevelType >  External references

	        FOREACH (erefer IN cmp.topLevelType.externalReferences |
	            MERGE(CPtpLevelType)-[:topLevelType_EReference]->
	                (ereferTL: eReferences {name:tolower(erefer.ref)})
	            SET ereferTL.ref = tolower(erefer.ref)
	        )
	        
	        // Inside bundle > packageFragment > compilationUnits -> topLevelType > Constructors

	        FOREACH (const IN cmp.topLevelType.constructors |
	            MERGE(CPtpLevelType)-[:topLevelType_Const]->
	                (constTL: Constructor {name:tolower(const.eClass)})
	            SET constTL.eClass = tolower(const.eClass),
	                constTL.visibility = tolower(const.visibility),
	                constTL.LOC = const.LOC
	        )
	        
	        // Inside bundle > packageFragment > compilationUnits -> topLevelType > methods

	        FOREACH (methd IN cmp.topLevelType.methods |
	            MERGE(CPtpLevelType)-[:Methods_Contains]->
	                (methodTL: Methods {name:tolower(methd.name)})
	            SET methodTL.eClass = tolower(methd.eClass),
	                methodTL.name = tolower(methd.name),
	                methodTL.visibility = tolower(methd.visibility),
	                methodTL.LOC = methd.LOC
	        )
	        
	        // Inside bundle > packageFragment > compilationUnits -> topLevelType > fields

	        FOREACH (field IN cmp.topLevelType.fields |
	            MERGE(CPtpLevelType)-[:Fields_Contains]->
	                (fieldTL: Methods {name:tolower(field.name)})
	            SET fieldTL.eClass = tolower(field.eClass),
	                fieldTL.name = tolower(field.name),
	                fieldTL.visibility = tolower(field.visibility),
	                
	                fieldTL.modify_0 = tolower(field.modifier[0]),
	                fieldTL.modify_1 = tolower(field.modifier[1])

	                
	                
	        )
	        
	    )
	)

	MERGE (v: Version {name:("Version " + p.version.major)}) SET 
	  v.className = tolower(p.version.eClass),
	  v.major=p.version.major, 
	  v.minor=p.version.minor,
	  v.micro=p.version.micro,
	  v.qualifier=tolower(p.version.qualifier)
	  
	 MERGE(b)-[:VersionNum]->(v)  
	 

	// Iterate through packages on ground level (fields inside packages are not completed)
	WITH {json} as document
	UNWIND document.packages AS s
	     MERGE (pkg: ext_packages {name:tolower(s.name), className:s.eClass}) 
	        SET pkg.qualifiedName = tolower(s.qualifiedName)

	MERGE(rce)-[:has_packages]->(pkg)
	 
	    // packages > fragments 
	    FOREACH (frag IN s.fragments | 
	       MERGE(fr: fragments {name:toLower(frag.ref)}) 

	     MERGE(pkg)-[:has_fragments]->(fr))
	     
	     // packages > subPackages
	     FOREACH (subpkg IN s.subPackages | 
	       MERGE(spkg: subPackages {name:toLower(subpkg.ref)}) 

	     MERGE(pkg)-[:has_subpackage]->(spkg))
	     
	     
	    // packages > parentPackage
	    FOREACH (ppkg IN s.parentPackage | 
	       MERGE(pp: parentPackage {name:toLower(ppkg.ref)}) 

	     MERGE(pkg)-[:has_parentPackage]->(pp))
	     
	     
	     
	// Iterate through services

	WITH {json} as document
	UNWIND document.services AS s

	MERGE (ser: services {name:tolower(s.interfaceName), className:s.eClass}) 
	        SET ser.interface = tolower(s.interface.ref)
	        
	MERGE(rce)-[:has_services]->(ser)

	// Iterate through externalTypes

	//WITH {json} as document
	//UNWIND document.externalTypes AS e
	 
	//MERGE (eTyp: eTypes {name:tolower(e.qualifiedName), className:tolower(e.eClass)}) 
	//MERGE(rce)-[:has_externalTypes]->(eTyp)
	'''


	# To get relations of particular node
	# MATCH (n:classes) where n.name='RCE Excel Component Execution' return (n)-[]->()

	#send query to the database
	graph.run(query, json=json_).data()

if __name__ == '__main__':

	convertJsonToNeo4j()