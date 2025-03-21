The SD (Structural Dependencies) folder contains the structural dependencies for each project. These dependencies are stored in CSV files, with each line representing two entities that form a dependency along with the calculated weight of that dependency. The folder includes:

	- structural_dep_hibernate.csv – Contains structural dependencies for Hibernate
	- structural_dep_ant.csv – Contains structural dependencies for Ant
	- structural_dep_catalina.csv – Contains structural dependencies for Catalina
	- structural_dep_gson.csv – Contains structural dependencies for Gson


The LD (Logical Dependencies) folder contains logical dependencies for each project. These dependencies are also stored in CSV format, where each line represents two entities that form a dependency along with the calculated weight. The folder includes:

	- ant_git_strength_X_ld.csv – Logical dependencies for Ant (X represents the strength threshold set)
	- catalina_git_strength_X_ld.csv – Logical dependencies for Catalina
	- gson_git_strength_X_ld.csv – Logical dependencies for Gson 
	- hibernate_git_strength_X_ld.csv – Logical dependencies for Hibernate 


Lastly, the baseline folder contains the baseline clustering solutions for each project.