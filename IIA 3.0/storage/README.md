# Storage Module Document
## Overview
The storage module is designed into three layers: **logic layer**, **custom layer** and **implementation layer**.  

The storage module is designed into three layers: logic layer, custom layer and implementation layer.  

The logical layer is mainly responsible for constructing the logical representation of the data, providing the basic necessary operations, and does not pay attention to the concrete implementation.  

The customization layer is responsible for implementing specific, concrete, highly variable content and allowing users to add their own plug-ins. The custom layer is the implementation scheme of logical layer.  

The implementation layer is concerned with transforming a logic-level solution into a storage-oriented implementation.  

The implementation layer provides many small modules, and the logic layer and the custom layer call these small modules for operations, so as to achieve the separation of logic and implementation.  

## Logic Layer
### Logic Layer Overview
The data type currently provided: **Repository**, **Sheet**, **Relation**.  

Repository is a piece space for specific kind of data. In the repository, the sheet could have relationship with each other and that's what we care about.  

Sheet is a unit in repository, we can input some highly structured data in the sheet.

Relation, after input data in the sheet, we maybe want to improve efficiency and reduce storage space. This step we need define relationship between sheets.

### Repository
1. Each repository have it's id(repo_id). 
