Search.setIndex({docnames:["analysis","bcc_build","build","coordination_number","correlation","file_rw","fitting_functions","genmdp","gentop","gromacs","hbonds","hexagonal_build","index","input","llclib","monomer_prep","msd","p2p","physical","place_solutes_pores","prep","rand","rdf","requirements","sampling","setup","solvation_equilibration","stats","timeseries","topology","transform","xlink","xlink_schemes","ztrace"],envversion:51,filenames:["analysis.rst","bcc_build.rst","build.rst","coordination_number.rst","correlation.rst","file_rw.rst","fitting_functions.rst","genmdp.rst","gentop.rst","gromacs.rst","hbonds.rst","hexagonal_build.rst","index.rst","input.rst","llclib.rst","monomer_prep.rst","msd.rst","p2p.rst","physical.rst","place_solutes_pores.rst","prep.rst","rand.rst","rdf.rst","requirements.rst","sampling.rst","setup.rst","solvation_equilibration.rst","stats.rst","timeseries.rst","topology.rst","transform.rst","xlink.rst","xlink_schemes.rst","ztrace.rst"],objects:{"":{file_rw:[5,2,0,"-"],fitting_functions:[6,2,0,"-"],gromacs:[9,2,0,"-"],p2p:[17,2,0,"-"],physical:[18,2,0,"-"],rand:[21,2,0,"-"],rdf:[22,2,0,"-"],sampling:[24,2,0,"-"],stats:[27,2,0,"-"],timeseries:[28,2,0,"-"],topology:[29,2,0,"-"],transform:[30,2,0,"-"]},"bcc_build.BicontinuousCubicBuild":{__init__:[1,1,1,""],determine_monomer_placement:[1,1,1,""],gen_grid:[1,1,1,""],place_monomers:[1,1,1,""],reorder:[1,1,1,""]},"correlation_function.Correlation":{__init__:[4,1,1,""],make_slice:[4,1,1,""],plot_slice:[4,1,1,""]},"genmdp.SimulationMdp":{__init__:[7,1,1,""],add_pull_groups:[7,1,1,""],write_em_mdp:[7,1,1,""],write_npt_mdp:[7,1,1,""],write_nve_mdp:[7,1,1,""],write_nvt_mdp:[7,1,1,""]},"gentop.SystemTopology":{__init__:[8,1,1,""],add_residue:[8,1,1,""],remove_residue:[8,1,1,""],write_top:[8,1,1,""]},"hbonds.System":{__init__:[10,1,1,""],identify_hbonds:[10,1,1,""],plot_hbonds:[10,1,1,""],set_eligible:[10,1,1,""]},"physical.region":{__init__:[18,1,1,""],xyregion:[18,1,1,""]},"rdf.System":{__init__:[22,1,1,""],bootstrap:[22,1,1,""],build_com:[22,1,1,""],build_spline:[22,1,1,""],plot:[22,1,1,""],radial_distribution_function:[22,1,1,""]},"solvation_equilibration.System":{__init__:[26,1,1,""],calculate_pore_water:[26,1,1,""],equilibrate:[26,1,1,""],full_equilibration:[26,1,1,""],place_water_tails:[26,1,1,""],query_database:[26,1,1,""],write_final_pore_configuration:[26,1,1,""]},"stats.Cdf":{__init__:[27,1,1,""],cdf:[27,1,1,""],random_sample:[27,1,1,""],update_cdf:[27,1,1,""]},"timeseries.VectorAutoRegression":{__init__:[28,1,1,""]},"topology.LC":{__init__:[29,1,1,""]},"topology.ReadItp":{__init__:[29,1,1,""],atoms:[29,1,1,""],get_bonds:[29,1,1,""],get_improper_dihedrals:[29,1,1,""],get_vsites:[29,1,1,""],organize_bonds:[29,1,1,""]},"topology.Residue":{__init__:[29,1,1,""]},"xlink.System":{__init__:[31,1,1,""]},"xlink_schemes.Dibrpyr14":{__init__:[32,1,1,""]},"xlink_schemes.DieneScheme":{__init__:[32,1,1,""],determine_reaction_type:[32,1,1,""],head2tail:[32,1,1,""],radical_c2:[32,1,1,""],terminate:[32,1,1,""]},"xlink_schemes.XlinkReaction":{__init__:[32,1,1,""]},bcc_build:{BicontinuousCubicBuild:[1,0,1,""]},correlation_function:{Correlation:[4,0,1,""]},file_rw:{write_assembly:[5,3,1,""],write_em_mdp:[5,3,1,""],write_gro:[5,3,1,""],write_gro_pos:[5,3,1,""],write_water_ndx:[5,3,1,""]},fitting_functions:{cdf_exp:[6,3,1,""],cdf_power_law:[6,3,1,""],exponential_integrated:[6,3,1,""],fit_power_law:[6,3,1,""],gaussian_log_likelihood:[6,3,1,""],hurst_autocovariance:[6,3,1,""],line:[6,3,1,""],log_power_law:[6,3,1,""],power_law:[6,3,1,""],power_law_discrete_log_likelihood:[6,3,1,""],powerlaw_integrated:[6,3,1,""],zeta:[6,3,1,""]},genmdp:{SimulationMdp:[7,0,1,""]},gentop:{SystemTopology:[8,0,1,""]},gromacs:{insert_molecules:[9,3,1,""],simulate:[9,3,1,""]},hbonds:{System:[10,0,1,""]},p2p:{avg_pore_loc:[17,3,1,""],p2p:[17,3,1,""],p2p_stats:[17,3,1,""],restrict_atoms:[17,3,1,""]},physical:{avg_pore_loc:[18,3,1,""],center_of_mass:[18,3,1,""],compdensity:[18,3,1,""],conc:[18,3,1,""],distance_from_pore_center:[18,3,1,""],limits:[18,3,1,""],minimum_image_distance:[18,3,1,""],p2p:[18,3,1,""],partition:[18,3,1,""],put_in_box:[18,3,1,""],radial_distance_spline:[18,3,1,""],region:[18,0,1,""],residue_center_of_mass:[18,3,1,""],thickness:[18,3,1,""],trace_pores:[18,3,1,""],wrap_box:[18,3,1,""]},rand:{randombeta:[21,3,1,""],randombetavariate:[21,3,1,""],randombinomial:[21,3,1,""],randomdirichlet:[21,3,1,""],randomexponential:[21,3,1,""],randomgamma:[21,3,1,""],randomgammaint:[21,3,1,""],randomnormal:[21,3,1,""]},rdf:{System:[22,0,1,""],grps:[22,3,1,""]},sampling:{approximate_discrete_powerlaw:[24,3,1,""],discrete_powerlaw_ccdf:[24,3,1,""],exact_discrete_power_law_sample:[24,3,1,""],random_exponential_dwell:[24,3,1,""],random_power_law_dwell:[24,3,1,""]},solvation_equilibration:{System:[26,0,1,""]},stats:{Cdf:[27,0,1,""],confidence_interval:[27,3,1,""],outliers:[27,3,1,""]},timeseries:{VectorAutoRegression:[28,0,1,""],acf:[28,3,1,""],acf_slow:[28,3,1,""],autocov:[28,3,1,""],bootstrap_msd:[28,3,1,""],calculate_moving_average:[28,3,1,""],correlograms:[28,3,1,""],msd:[28,3,1,""],msd_straightforward:[28,3,1,""],step_autocorrelation:[28,3,1,""],switch_points:[28,3,1,""]},topology:{LC:[29,0,1,""],ReadItp:[29,0,1,""],Residue:[29,0,1,""],fix_names:[29,3,1,""],map_atoms:[29,3,1,""]},transform:{Rvect2vect:[30,3,1,""],monoclinic_to_cubic:[30,3,1,""],random_orientation:[30,3,1,""],rescale:[30,3,1,""],rotate_coords:[30,3,1,""],rotate_coords_x:[30,3,1,""],rotate_coords_z:[30,3,1,""],rotate_vector:[30,3,1,""],rotate_x:[30,3,1,""],rotate_z:[30,3,1,""],rotateplane:[30,3,1,""],rotateplane_coords:[30,3,1,""],translate:[30,3,1,""]},xlink:{System:[31,0,1,""],Topology:[31,0,1,""]},xlink_schemes:{Dibrpyr14:[32,0,1,""],DieneScheme:[32,0,1,""],XlinkReaction:[32,0,1,""]}},objnames:{"0":["py","class","Python class"],"1":["py","method","Python method"],"2":["py","module","Python module"],"3":["py","function","Python function"]},objtypes:{"0":"py:class","1":"py:method","2":"py:module","3":"py:function"},terms:{"1st":[28,32],"30degre":10,"3x3":5,"4x4":30,"4y2_":[],"50th":32,"5b06130":12,"5y1_":[],"8b09944":12,"9b04472":12,"abstract":31,"boolean":18,"break":2,"case":[4,6,7,8,12,15,17,18,21,22],"class":[12,13],"default":[2,4,7,8,9,10,13,17,22,26,27,30,31],"final":[9,26,31],"float":[1,4,6,7,10,11,17,18,21,22,24,26,28,30,31],"function":[0,2,12],"import":[4,10,12,22,27,28,30],"int":[1,4,6,7,8,10,11,17,18,21,22,24,26,28,29],"long":[7,26],"new":[1,8,31,32],"return":[5,6,9,11,17,18,21,22,24,27,28,29,30,32],"short":[26,31],"switch":[17,28],"true":[2,4,6,7,8,9,10,11,13,18,22,26,28,29,31,32],"var":[11,28],"while":[18,22,26],ACS:12,Axes:26,But:28,For:[11,12,15,22,26,28,31,32],Not:[4,31],One:[7,8,23],RES:4,That:15,The:[1,4,5,6,9,10,12,15,18,22,23,26,28,31,32],There:[15,31],These:[17,21,32],Use:[10,17],Used:6,Useful:[12,17],Uses:21,Using:[12,15],Will:[4,18],__init__:[1,4,7,8,10,11,18,22,26,27,28,29,31,32],a_1:[],a_i:[],a_p:[],abl:15,about:[4,15,17,28,30],abov:[6,15,26,31],abs:24,absolut:11,acc:10,accept:[10,26],acceptor:[10,15],acceptor_onli:10,acceptoratom:10,access:[],accord:[4,7],accordingli:7,account:29,accur:[13,22,32],acf:28,acf_slow:28,achiev:26,acs:12,acsnano:12,activ:31,actual:32,adapt:12,add:[7,8,9,26,27,31],add_pull_group:7,add_residu:8,added:[7,13,15,31],adding:[28,32],addit:[29,31,32],adjac:[2,11,22,26],adjust:[7,11,26,31],advantag:15,after:[28,30,31,32],aftercalcualt:10,algorithm:[5,7,31],align:[11,12],align_plan:11,align_with_x:11,alignment_vector:30,alkan:[18,32],all:[1,4,5,7,10,12,17,18,22,23,28,29,30,31,32],allow:[10,28],alon:12,along:[1,4,18,26,28],alpha:[6,24,27],alreadi:[7,32],alwai:[13,15],amber:23,ammonium:12,amount:[1,12,15,26],amphiphil:12,amplitud:4,anaconda:23,analys:12,analysi:[4,6,10,12,14,22],analyt:6,analyz:[10,22],andion:17,angl:[2,4,10,11,18,26,30,31,32],angle_averag:4,angle_cut:10,ani:[1,8,10,12,15,23,31],annot:[10,22,29],anomal:24,anoth:[7,31,32],answer:[15,28],antechamb:23,anyth:[4,18],appear:[18,32],appendix:24,appli:[7,10,12,15,26,30,32],applic:12,approach:15,appropri:[8,12,26,31],approxim:[2,18,24],approximate_discrete_powerlaw:24,area:[6,22],arg:[4,10,17,18],argpars:12,argument:[9,12,15],around:[4,12],arrai:[4,5,6,11,17,18,24,27,28,30],arrang:1,array_lik:21,ascii:17,assembl:[5,8,12,31],associ:[4,28,29],assum:[7,18,28,29],atom:[1,4,5,10,11,15,17,18,22,26,29,31,32],atomist:[2,22],atomst:12,attach:32,attempt:[10,32],attribut:[11,15,28,29,30,32],august:12,auto:17,auto_exclud:17,autocorrel:28,autocov:28,autocovari:[6,28],autogress:28,automat:[4,15,17],autoregress:28,avail:23,averag:[4,17,18,22,28,30],avg_pore_loc:[17,18,22],avoid:32,awai:[15,31],awar:28,axes:[4,26],axi:[4,6,7,11,18,22,26,28,30],back:18,bar:[4,18,22],barostat:[7,13],base:[1,4,6,10,11,15,18,21,22,28,29,30,31,32],basic:[4,22],bcc:[2,7,13],bcc_build:1,bcoscia:4,becam:23,becaus:[12,32],becom:[15,31],been:[7,12,23,26,32],befor:[12,13,15,18,30,31],begin:[4,10,15,17,22],behavior:28,being:[5,7,10,18,32],believ:15,belong:[22,26],below:[4,10,15,26],benjamin:12,benzen:[17,29],berendsen:[7,13,17,26],berendsenpressur:26,best:15,beta:21,between:[0,2,4,6,10,11,18,22,26,28,30,31,32],betweenbox:[2,26],betweenstack:2,beyond:18,bicontin:7,bicontinu:[1,2,7,12,13],bicontinuouscubicbuild:1,big:28,bin:[4,6,18,22],binari:23,binomi:21,bisect:26,black:[4,22],blank:4,block:26,block_radiu:4,blue:22,bmatrix:[],bond:[0,29,31,32],bonds_with:32,book:21,bool:[4,7,8,10,11,18,22,26,28,29,32],bootstrap:[17,22,27,28],bootstrap_msd:28,both:[4,17],bottom:[17,18,31],bound:[6,11,24,26,27],box:[1,2,4,5,8,11,18,21],box_length:2,brian:12,bridg:31,broaden:4,brownian:6,buffer:[17,18],build:[5,12,13,15,22,25,26,29],build_column:11,build_com:22,build_mon:[13,29,31],build_monom:[2,26],build_monomer_residu:22,build_splin:22,buildhexagon:11,buildhii:22,built:[11,12,26,31],c1_atom:29,c2_atom:29,c44:32,c45:32,calcul:[0,4,6,10,11,12,15,17,18,22,24,26,27,28,29,30,32],calculate_correlation_funct:4,calculate_moving_averag:28,calculate_pore_wat:26,calcult:28,call:[13,31],callabl:27,can:[6,7,8,10,12,13,15,21,23,26,28,30,31,32],cannot:12,captur:15,carbon:[4,15,22,29,31,32],care:[17,32],carri:12,categori:[],cdf:[21,24,27],cdf_exp:6,cdf_power_law:6,cdotcdotcdot:10,cell:[1,2,4,5,12,17,18,22,26,29,30,32],center:[2,4,11,15,17,18,22,26,28,29,31],center_of_mass:[4,18],certain:[17,26],ch5f_slide:21,chain:32,chain_numb:32,chandler:10,chang:[7,26,32],charg:29,check:[10,13,17,27],chemic:12,chemistri:[12,32],chinedum:12,choic:[7,17,26,32],choo:12,choos:[1,4,11,17],chosen:[1,2,31,32],christoph:12,circl:[4,22],cite:10,clean:32,close:[1,9,26],closest:[15,18,26],clunki:15,cm1013027:12,cm3:2,code:[15,26,32],coeffici:[6,28],color:4,column:[2,4,11,15,26],columnar:11,com:[4,7,18,22,27],combin:[31,32],come:[6,23],command:9,comment:15,common:31,commonli:28,comp:18,comparison:22,compdens:18,complementari:24,complet:10,complex:[12,28],compon:[17,18,22,31],compos:12,composit:26,compress:22,conc:18,concaten:17,concav:2,concentr:[18,22,26],condit:10,conduct:12,confid:[22,27,28],confidence_interv:27,config:26,configur:[4,7,9,13,15,17,25,31,32],confin:12,confirm:[22,32],connect:[29,32],consensu:10,consid:[10,15,18,31],consist:[12,28,32],constant:[6,7,13,26,30],constitu:[4,15,22,32],constitut:22,construct:[12,18,32],contain:[4,12,17,18,26,27,28,30,31,32],content:26,context:[10,15,32],continu:12,control:[1,6,7,26,32],conveni:[7,8,12,13,26],converg:[7,26,31],convert:[29,30,32],convex:2,coord:[7,13,18,30],coord_group:7,coordin:[0,1,4,5,7,8,9,10,11,13,14,15,17,18,22,23,26,31],coplanar:15,core:17,corner:18,correct:26,correl:[0,2,11,28],correlation_funct:4,correlation_length:[2,11],correlogram:28,correspond:[5,32],coscia:12,could:[28,31],count:[8,18,22],coupl:[7,13,31],cours:28,coval:10,covari:28,covariance_j:28,cowan:12,creat:[1,4,7,8,11,12,15,22,28,29,31],criteria:[10,31],criterion:10,critic:27,cross:[5,8,12,25,28,29],crosslink:[7,12,13,29,31],crystal:[2,4,20,26,29],cse:21,cubic:[1,2,5,7,12,13,30],cumul:[24,27],current:[2,4,17,22,26,28],curv:[6,28],curvatur:[1,2],cut:[6,10,18,22],cutoff:[18,31],dat:9,data:[6,22,26,27,28,29],databas:[9,26],date:12,dbwl:[2,26],deal:28,debug:21,decai:[4,6,24],decemb:12,decid:[9,15,17],decis:26,decompos:31,decomposit:[9,31],decreas:[26,31],defin:[2,10,11,13,15,18,22,29,30,31,32],definit:10,degre:[2,10,11],demonstr:24,den:2,densiti:[1,2,9,18,22,31],depend:[6,10,12,28],der:9,deriv:1,descent:5,describ:[1,4,7,8,10],describingassembl:31,descript:[8,15,29],design:31,desir:[8,11,22,26,30],detail:28,detect:17,detectequilibr:17,determin:[1,2,4,15,17,22,26,28,29,32],determine_monomer_plac:1,determine_reaction_typ:32,dev:28,develop:21,deviat:[17,18],dfrac:6,dha:10,diagram:10,dibrpyr14:32,dict:[29,32],dictionari:[29,32],dien:32,dieneschem:32,differ:[8,21,32],dihedr:[29,32],dim:[7,28,30],dimens:[1,4,5,15,18,28,30,31],dimension:28,dipol:7,direct:[1,2,4,8,11,12,15,18,26,28,29,30],directli:[5,10,15],directori:[8,12,32],disching:12,discplac:28,discret:[6,24,28],discrete_powerlaw:24,discrete_powerlaw_ccdf:24,disk:5,disord:4,displac:[0,11,26,28],displai:[10,22],disproportion:31,dist:18,distanc:[0,1,2,4,7,10,11,15,18,22,26,31],distance_from_pore_cent:18,distinct:[17,18,32],distinguish:32,distribut:[0,6,11,14,18,21,27,28,31],div898:27,divid:22,doc:28,docstr:32,document:[7,23],doe:[6,12,15,32],doesn:21,doi:[12,24],doing:22,domain:[9,31],domain_decomposit:31,domin:32,don:4,donat:10,done:[12,26],donor:[10,15],donor_onli:10,donoratom:10,donors_onli:10,doubl:[17,32],dougla:12,down:22,download:23,draw:[21,24,27],drop:17,due:21,dummi:[29,31,32],dummy_bond:32,dummy_connect:32,dummy_mass:32,dummy_nam:31,dummy_residu:31,dure:[7,13,15,26,31],dwell:24,dynam:[9,10,13,28],each:[1,2,4,5,10,12,17,18,22,26,28,29,31,32],eachcolumn:[2,26],easier:22,easiest:4,easili:10,eda35h1:27,eda:27,edg:[1,6,22],edit:28,edu:21,educ:26,effect:1,effici:31,effort:[1,12,31],egin:[],electron:31,elementari:30,elig:[31,32],elimelech:12,elimin:31,elsewher:32,em_energi:9,em_step:[7,13,31],emper:[6,27],enclos:18,end:[4,10,17,22],energi:[5,7,9,13,26,31],energyminim:31,ensembl:[7,13,28],enter:[4,18],entir:32,entri:[26,32],enumer:10,epub:24,equal:[4,22,23,28,31],equat:28,equil:17,equilibr:[17,26],equival:21,error:[6,15,26,27,28],errorbar:27,especi:10,estim:[6,18,28],etc:[1,2,7,31,32],euclidean:22,evalu:[6,24,27],evan:12,even:[4,32],everi:[4,10,17,22],everyth:32,exact:24,exact_discrete_power_law_sampl:24,exactli:4,exampl:[11,15,32],except:12,exclud:[17,18],exist:[10,29],expect:[4,28],experiment:1,expnonenti:6,expon:[4,6,24],exponenti:[4,6,21,24],exponential_integr:6,extend:[11,26],extens:[4,22,26,29],extra:[7,13,15,31],extract:29,extrus:18,fabric:12,factor:[4,9,28],fals:[1,2,4,5,6,7,8,9,10,13,17,18,22,24,26,27,28,29,31,32],far:[4,12,26],faster:[24,28],fbm:23,feng:12,fft:28,field:[12,23],figur:8,file:[2,4,9,10,11,12,14,15,17,18,22,23,25,26,29,31,32],file_rw:5,filenam:18,fill_between:27,film:12,filtrat:12,find:[17,18,30,32],first:[4,6,10,22,28,32],fit:[4,14,28],fit_power_law:6,fitting_funct:6,fix:[18,29],fix_nam:29,flag:[4,7,10,17],flowback:12,focu:12,folder:31,follow:[4,7,8,13,27,29,32],forc:[7,13,23,26,31],force_convert:29,forcefield:[8,31],forev:7,form:[2,4,6,10,12,21,24,26,32],format:[2,5,8,11,17,18,22],fourier:[],fraction:[6,17,18],fractur:12,frame:[4,5,7,10,13,17,18,22,28],frame_no:5,free:31,freez:5,freeze_dim:5,freeze_group:5,frequenc:[7,13],frequent:12,from:[2,4,5,6,7,8,9,10,11,13,15,17,18,21,22,24,26,27,28,29,30,31,32],frp:31,ftp:21,fucnction:21,full:[2,4,8,12,26,29],full_equilibr:26,fulli:[5,12,26],fully_solv:26,functionabout:4,further:18,furthest:15,ga3c11:17,gabriel:12,gaff:[8,23,31],gamma:[6,21],gap:18,gaussian:[6,11,28],gaussian_log_likelihood:6,gemini:12,gen_grid:1,gener:[4,5,12,14,17,22,23,24,25,26,27,28,30,31,32],genmdp:7,gentop:8,genvel:7,geometr:10,geometri:[7,10,11,12],get:[4,5,11,14,26,27],get_bond:29,get_improper_dihedr:29,get_vsit:29,gin:12,github:4,give:[5,12,15,28],given:[4,6,11,12,13,15,21,30,32],glaser:12,glycerol:2,gmx:[4,23],goe:29,google_rich_qa:27,gov:27,gpu:31,gracia_quest_2013:10,greater:[23,31],grid:[1,2,9,18,31],gro:[2,4,5,7,8,9,10,11,13,17,18,22,26,29,31,32],gromac:[4,10,12,14,15,22,25,26,29],group:[1,2,4,5,7,11,12,15,17,22,26,30,31,32],grp:22,grubb:27,guess:26,guess_rang:26,guess_strid:26,guid:7,gyroid:[1,2],hamilton:28,handbook:27,happen:31,hard:32,has:[5,7,10,12,13,26,29,31,32],hasn:26,hatakeyama:12,have:[6,12,18,23,26,31,32],hbond:[10,15],head2tail:32,head:[2,4,11,17,22,26,32],heavili:23,hei:[],help:[15,26],here:[12,22,27],hexagon:[2,11,12,17,22],hexagonal_build:11,high:12,highest:[6,17,26],highlight:4,hii:[2,4,10,12,15,17,22,25,26,31],hiid:31,histogram:[4,22],hoh:[10,26],hold:32,home:4,how:[7,12,15,26,29,31],howev:[4,7,8,12,31],htm:27,html:[7,28],http:[7,12,21,24,27,28],hurst:6,hurst_autocovari:6,hurwitz:[6,24],hybrid:[15,32],hydraul:12,hydrogen:[0,31,32],hydrogen_connect:32,hydrophil:[1,12],hydrophob:1,ideal:12,identifi:[0,8,15],identify_hbond:10,ids:5,illustr:[15,26],imag:[12,18,29],implement:[2,4,17,21,24,27,32],implic:12,implicit:2,improp:[29,32],inarg:10,includ:[4,6,8,10,17,18,22,23,28,31,32],incorpor:22,independ:[6,28],index:[5,12,17,22,32],indic:[5,18,27,28,29,32],individu:[18,28],infin:6,info:[15,17],inform:[14,15,26],inher:12,inidividu:8,initi:[7,10,13,15,25,29,31],initial_configur:31,inner:18,input:[4,6,7,8,10,12,17,25,30,31],input_fil:26,insert:[9,26],insert_molecul:9,insid:[5,18],instal:23,instead:[15,21,28,32],instruct:[12,23],integ:[4,6,21,29],integr:[6,28],intend:12,intens:4,interact:[6,12,15,17],intercept:6,interconnect:12,interest:[10,12],interfac:[1,2],intermedi:31,interv:[22,27],inth:17,intiat:31,intuit:[12,32],invers:21,invert:[1,2,4,12],involv:[5,10,15,29,31,32],isn:[21,28],isotrop:[7,12],issu:31,iter:31,itl:27,itp:[4,7,8,15,29,31,32],its:[6,12,17,30,32],jain:21,jame:[12,28],januari:12,jenni:12,joint:28,joint_distribut:28,joseph:12,journal:12,jpcb:12,june:12,just:[1,15,28],karl:12,keep:[1,4,5],kei:[29,32],kwarg:18,l_berendsen:26,l_nvt:26,l_pr:26,label:[15,22,32],lag:28,lam:24,larg:[12,15,28],largest:[22,28],largest_prim:28,last:[4,10,22,28,29,32],law:[6,24],layer:4,learn:12,leav:4,left:[6,12],legend:22,length:[1,2,4,5,7,11,13,18,24,26,28,30,31],length_berendsen:26,length_nvt:26,length_parrinello_rahman:26,lengthwil:4,less:[4,10,26],librari:[5,27,30],lie:1,like:[],likelihood:6,limit:[4,18,24],linden:12,line:[2,6,17,18,29],lineatom:11,lineextend:[2,26],link:[5,8,12,25,29],linkabl:32,linksthat:31,liquid:[2,4,20,26,29],list:[1,4,5,7,10,12,17,22,26,27,28,29,32],llc:[2,10,12,17,22,31],llc_membran:[1,4,8,10,11,12,22,23,27,28,30],llclib:[1,8,11,12,27,28,30],load:[4,10,18,22,29,30],locat:[1,4,6,8,11,15,17,18,22,30,31],log:6,log_power_law:6,lohr:12,longer:4,look:[22,32],loop:26,lose:28,lower:[4,6,24,27],lowest:26,lpha:6,lpr:26,luzar:10,luzar_effect_1996:10,lvar:2,machin:23,made:[12,26,31,32],magnet:12,mai:[23,31,32],main:[4,31],make:[4,6,10,11,12,18,22,26,29,31,32],make_slic:4,mani:[21,31],manipul:[],manual:[7,17,23,32],map:[29,32],map_atom:29,marissa:12,mass:[4,15,18,22,28,29,32],mass_atom:18,match:30,materi:12,math:[],mathemat:24,matlab:21,matplotlib:4,matric:[28,30],matrix:[5,28,30],matter:29,matthew:12,max:[18,31],maxim:6,maxima:4,maximum:[6,10,18,22,31],maxwelldistribut:7,mayb:22,mdp:[5,9,13,25,26,31],mdp_em:31,mdp_nvt:31,mdrun:31,mdtraj:[5,10,17,18,23,29,30],mean:[0,1,2,6,7,11,27,28,32],meancurvatur:2,meant:[18,31],measur:[4,18],mechan:[12,31],meijuan:12,membran:[1,2,5,17,18,22],memsci:12,menachem:12,mesophas:12,met:31,method:[2,21,24,28],michael:12,might:[6,10,24],min:18,minim:[5,6,7,13,31,32],minimum:[18,29],minimum_image_dist:18,minimz:[9,26],mix:2,model:[12,28],modul:[12,23,28],mol:[7,26],molecul:[8,11,12,23,26,30],molecular:[9,10,12,13,29,31],monoclin:[4,18,30],monoclinic_to_cub:30,monom:[1,2,4,5,7,10,11,12,13,17,22,23,26,29,31,32],monomer_top:4,monomerhead:[2,26],monomers_per_column:[2,26],monomers_per_lay:4,monomerstructur:2,more:[4,7,8,12,15,22,24,26,28,30,32],most:[4,7,8,12,15,22,23,27,31],move:[18,28,31],mpi:[9,26,31],msd:[6,28],msd_straightforward:28,much:24,muller:21,multidimension:28,multipl:[4,17,22,28,32],multipli:9,multivari:[11,28],must:[1,10,15,31,32],n_atom:18,n_com:18,n_data_point:27,n_dimens:28,n_frame:28,n_particl:28,n_trajectori:27,nacarb11v:[4,13,22,26],nacarb11vd:31,naga3c11:22,name:[1,5,9,11,18,23,29,32],nano:12,nanofiltr:12,nanopor:12,nanoscal:12,nanostructur:12,natom:[5,18,28,29,30],nbin:[18,22],nboot:[17,22],nchain:32,ncolumn:[2,26],ncom:18,ncompon:[17,18],ndarrai:[5,6,11,17,18,22,28,30],ndx:28,necessari:[31,32],necessarili:28,need:[6,7,10,12,15,18,23,26,31],neg:2,nejati:12,network:12,nevertheless:12,newcross:31,next:[12,26],nframe:[17,18,28,30],nist:27,nlayer:11,nn505037b:12,no_column_shift:2,no_mon:5,no_por:[17,18],no_vsit:29,nobl:12,nogenvel:13,nois:[6,28],none:[4,5,7,9,10,18,22,24],nonetyp:10,nopor:[2,26],normal:[1,2,6,11,21,22],noshow:[4,10,17,22],note:[7,10,12,21,28,29],now:[7,27,32],np2p_distanc:17,npoint:[18,28],npore:[11,17,18,22],nproc:[26,31],nprocess:9,npt:[7,13,18,30],npts_spline:[18,22],npz:22,nres_atom:29,nseri:28,nstenergi:[7,13],nstfou:7,nstfout:[7,13],nstvout:[7,13],nstxout:[7,13],nth:17,number:[0,1,2,4,5,6,7,8,9,10,11,13,14,17,18,22,24,26,27,28,29,31,32],numberof:31,numer:6,numpi:[5,17,18,21,26,28,30],nve:7,nvt:[7,26,31],object:[5,8,10,11,17,18,28,29,30],obs:27,observ:[27,28],obtain:[11,18,23],occur:[12,17,28],ofarg:4,ofeach:22,off:[4,10],offset:4,ofmembran:17,often:17,onc:12,one:[1,12,15,21,26,28,31,32],onli:[2,4,6,7,10,13,15,17,18,21,22,24,26,27,31,32],onto:22,opposit:[2,6,17],option:[4,7,13,22,29,30],order:[4,5,10,12,15,18,22,26,27,28,29,31,32],org:[7,12,24,28],organ:[23,27],organize_bond:29,orient:[12,15,30],origin:[4,11,15,30,32],osuji:12,other:[4,12,21,22,31,32],otherwis:[10,17,29],our:[12,15,22,23,31],ourselv:15,out:[2,4,5,7,8,9,11,12,18,26,31],outlier:27,output:[2,4,5,7,8,9,11,12,13,17,22,26,28,30],output_gro:31,outsid:18,over:[2,18,30,32],overrid:[4,17],own:[6,32],p2p:[2,11,17,18,26],p2p_stat:17,p_center:[17,18],p_coupl:7,pack:[11,12],packag:[10,15,23],pag:28,page:[12,13,23],pair:[31,32],pairwis:17,parallel:[9,26,29,31],parallel_displac:[2,26],parallelogram:17,param:[1,5,6,18,24,27,28,30],paramet:[1,4,5,6,7,8,9,10,11,17,18,21,22,24,26,27,28,29,30,31,32],parameter:[12,23],paramt:[9,21],parmeter:15,parrinello:26,pars:15,part:[10,15,18,22],particip:[10,15],particl:[4,7,18,28],particular:27,partit:18,pass:[10,12,15,29],past:28,path:[8,10,17],pbc:4,pcenter:18,pcoupltyp:[7,13],pda:15,pdb:[17,22,29],pdf:[21,22,24],peak:4,peak_loc:4,per:[4,10,26,28,29],percent:[1,26,27,31],percentag:31,percentil:28,perfect:4,perform:[12,24,26,31],perhap:32,period:29,perpendicular:[1,15,18],persist:[2,11],phase:[2,12,15,22,25,32],phenyl:15,physic:[12,14,22],pic1:[],pickl:[10,18],picosecond:7,pictur:15,pip:23,place:[1,4,9,11,15,18,25,26,29,30],place_monom:1,place_water_tail:26,placement:30,plan:12,planar:[15,32],plane:[2,11,15,18,22,29,30],plane_indic:11,plot:[0,1,2,4,10,17,18,22,27,28],plot_avg:17,plot_everi:17,plot_grid:2,plot_hbond:10,plot_rang:4,plot_slic:4,plot_std:17,plt:27,png:10,point:[1,2,6,11,15,18,22,26,27,28,30],polygon:18,polym:12,polymer:[12,31],polymeriz:12,poop:[],pore:[0,1,2,11,12,15,18,22,25,26,29],pore_alpha:11,pore_cent:[18,22],pore_radiu:[2,11,26],port:21,pos:[5,17,18,30],posit:[0,2,4,5,8,11,17,18,26,28,30],possibl:21,post:12,potenti:[1,10,31],power:[6,24],power_law:6,power_law_discrete_log_likelihood:6,powerlaw:6,powerlaw_integr:6,practic:15,prada:10,pre:15,preced:18,predefin:17,prepar:[4,12],preprocess:4,presenc:12,present:[7,12,29],pressur:[7,13,26],prevent:17,previou:28,previous:4,primari:12,prime:28,principl:15,print:9,probabl:[7,8,11,21,27,28,31],problem:27,proce:31,procedur:[15,31],process:[9,12,15,26,28,31,32],processess:31,produc:28,productof:31,progag:31,program:32,progress:[18,22],prone:15,propag:31,proper:[10,15],properli:10,properti:14,propos:10,protein:9,provid:10,proxim:[26,31],pseudocod:26,pseudorandom:21,pull:[7,24],purpos:[4,15,18,24],put:[5,7,8,13,18,26],put_in_box:18,pycharmproject:4,pymbar:17,pypi:23,python:[12,21,26,27],qii:[1,2],query_databas:26,question:27,quickli:28,rad_frac_term:31,rad_perc:31,radial:[0,18],radial_distance_splin:18,radial_distribution_funct:22,radic:[31,32],radical_c2:32,radical_reaction_percentag:31,radical_reaction_weight:32,radical_termination_fract:31,radii:[9,26],radiu:[2,4,15,18,26,29],rahman:26,rand:21,randdirichlet:21,random:[2,11,14,24,26,27],random_exponential_dwel:24,random_orient:30,random_power_law_dwel:24,random_sampl:27,random_se:[2,26],random_shift:11,randombeta:21,randombetavari:21,randombinomi:21,randomdirichlet:21,randomexponenti:21,randomgamma:21,randomgammaint:21,randomli:[2,11,14,15,26,30],randomnorm:21,rang:[4,26],rate:[6,7,24],rather:15,ratio:26,rdf:[18,22],react:[31,32],reacted_typ:32,reaction:[15,31],reaction_percentag:31,reaction_weight:32,read:[8,14,26,29],readabl:32,readili:[27,31],readitp:29,real:[12,31],realist:4,realiz:28,recogn:32,recommend:[22,23,32],reduct:28,ref:18,ref_atom:18,ref_atom_index:11,ref_group:7,refer:[7,15,18,29,30,32],region:[18,26],reject:27,rel:[27,32],relat:4,relationship:4,relev:[29,32],remov:[1,8,32],remove_residu:8,renam:28,render:22,renumb:32,reorder:[1,11],rep:22,repeat:31,repres:[12,22,29,31],represent:10,reproduc:[2,11],requir:[12,26,32],res:[4,5,10,18,31],resampl:22,rescal:30,resd:31,residu:[1,4,5,8,10,11,13,18,22,26,29,31,32],residue_1:22,residue_2:22,residue_center_of_mass:18,residue_nam:4,respect:[2,4,11,12,18,29,30,32],respons:4,restrain:[7,8,26],restrained_top_nam:8,restraint:[7,8,13,26],restraint_axi:26,restraint_residu:26,restrict:[10,17,22],restrict_atom:17,result:[2,22,28,31],richard:12,right:[6,12,27],ring:[15,26,29],ring_restraint:26,ring_restraintatom:26,rise:15,rm_improp:32,robust:12,rosenblum:12,rotat:[29,30],rotate_coord:30,rotate_coords_x:30,rotate_coords_z:30,rotate_vector:30,rotate_x:30,rotate_z:30,rotateplan:30,rotateplane_coord:30,routin:5,rtype:[6,24,29,30],run:[4,7,8,9,12,13,17,26,28,31],ruptur:23,rvect2vect:30,rwrite:26,same:[1,4,5,8,10,12,21,26,28,29,31,32],sampl:[14,17,27,28],sarah:12,save:[4,10,17,18,22,31],save_frequ:31,save_intermedi:31,savenam:[10,18,22],scalabl:12,scale:[4,6,9,12,21],scatter:1,scenario:4,scheme:[7,13,32],schwarzd:1,scienc:12,scipi:6,scratch:26,screen:[9,12,15],script:[7,8,12,13,15,17,21,22,23,26],search:[10,12,27],second:[28,29,30,32],section3:27,section:[2,8,12,29],see:[7,10,12,21,23,24,28,29,31,32],seed:[2,11,21,26],select:[10,12,15,17,26,31],self:[6,12,32],semiisotrop:[7,13],sens:6,separ:[1,4,10,11,12],sequenc:[26,28],sequenti:[18,31],seri:14,set:[2,6,12,18,30],set_elig:10,setup:12,shade:22,shape:[11,17,18,21],share:9,sharp:4,shift:[1,2,11,18,30],ship:23,shirt:12,should:[4,5,7,11,12,15,21,22,23,26,29,31,32],show:[1,4,10,17,18,22],shown:[4,15,18,29],siam:24,siamak:12,side:[17,18],sigma:[6,21],sign:6,similar:32,simpl:[12,15],simplifi:[31,32],simul:[7,8,9,10,13,17,26,30,31],simulationmdp:7,sinc:10,singl:[2,4,5,8,18,21,22,26,27,29,31,32],site:[29,31,32],size:[1,12,21,24],skip:[10,17,22],slice:[4,5],slope:[6,18],slow:[12,24],slower:22,small:12,smaller:28,sodium:17,soft:12,softwar:[10,12],sol:2,solut:[9,12,17,18,22,23,25,26],solvat:[5,7,13,17,25],solvated_fin:26,solvation_equilibr:26,solvent:[2,7,13],some:[10,18,23,27,29,32],somewher:30,sound:24,sp2:32,sp3:32,space:[1,4,15],space_group:1,spars:27,spatial:4,speci:[18,31],special:[7,8,17,22],specif:[4,15,17,22,27,29,30],specifi:[1,4,7,9,13,15,17,18,22,26,29,31],speed:[28,32],sphere:22,spike:4,spline:[18,22],spline_pt:22,spontan:12,spread:17,spt:22,sql:26,squar:[0,28],stabl:[12,26,31],stack:[2,4,11,15,26],stackoverflow:27,stage:12,stagnat:31,stand:12,standard:[17,29],start:[4,10,17,18,32],stat:27,state:[12,28],statist:[14,17,22],statsmodel:28,steepest:5,step:[5,6,7,13,15,27,28,31],step_autocorrel:28,still:[4,31,32],stop:[17,22,26],store:[29,32],str:[1,4,5,7,8,10,11,17,18,22,26,29,31,32],straightforward:28,stream:12,string:[5,29],structur:[5,11,12,13,29,31],structurefactor:4,studi:[10,12,18],sub:[12,29,32],subdiffus:6,subprocess:9,subtract:[15,32],success:[12,21],suffic:15,suffici:1,sum:6,summar:12,summit:31,superdiffus:6,supplement:12,suppli:17,sure:[4,10,26],surfac:[1,2],surfact:12,surround:4,switch_point:28,swithc:28,symbol:15,sys:[10,22,26],system:[2,4,5,7,8,10,11,12,13,17,18,22,26,28,29,31,32],systemtopolog:8,tabl:10,tabul:6,tail:[17,18,22,26,29,30,32],tail_end:17,tail_front:17,take:[4,5,7,13,15,28,32],taken:4,tau_p:[7,13],tau_t:[7,13],techniqu:[21,22],tediou:32,temp:[7,13,17],temperatur:[7,13,17,31],term:[6,24,28],term_prob:31,termin:[29,31,32],test:[12,22,23,26,27],texttt:10,than:[10,12,18,23,24,26,28,31],thanon:4,thei:[1,4,18,27,28,29,32],them:[12,13,15,30,32],therefor:[12,23],thermodynam:[7,13],theta:[4,11,18,30],thi:[1,2,4,5,6,7,8,9,10,13,15,17,18,21,22,24,26,27,28,29,30,31,32],thick:[17,18,22],thin:12,think:[10,26],thisto:2,those:[5,18,29,32],three:[12,15,31],through:[7,12,15,18,22,29],throughput:12,thu:1,tilt:[2,11],time:[7,10,13,14,15,17,18,22,24,26,31],time_step:7,time_uniform:6,timeseri:[17,28],titl:[7,13],toappli:26,todo:[6,8,22,32],togeth:31,tol:[18,21,26],toler:26,tomak:26,tool:[12,23],top:[4,8,9,12,17,18,22,31],top_descript:8,topnam:[8,31],topol:[8,31],topolog:[1,7,9,11,13,14,15,25,26,31,32],tortuou:12,total:[9,10,26],touslei:12,toward:15,tqdm:23,trace:[18,22],trace_por:18,track:[17,18],traj:[4,10,17,18,22],traj_whol:[4,22],trajectori:[4,5,6,7,10,12,13,15,17,18,22,23,27,28,30],transform:[14,28],translat:[1,11,15,30],translate_to_origin:11,transport:12,treatment:12,tree:12,trial:[17,21,22,28],trivial:12,trjconv:4,trr:[4,10,17,22],truncat:28,tsa:28,tupl:[4,6,7,26],turn:[7,13,21],two:[4,6,22,26,31,32],type:[6,7,13,15,18,24,28,30,31,32],typic:29,u1_t:[],u2_t:[],u_t:[],ucel:[5,11],umbrella:7,unclear:32,undefin:31,under:[6,8,10,22],underli:12,understand:[4,12],unfortun:21,uniform:[11,12,21],unit:[1,2,4,5,12,17,18,22,26,29,30,32],unitcel:[5,11,18,30],unitcell_vector:18,unitcellvector:30,unless:29,unreact:32,until:[7,31],updat:[10,26,31],update_cdf:27,upper:[4,24,27],upper_limit:[6,24],usag:[2,7,8,13,17,26,31],use:[4,5,7,8,10,13,17,22,24,26,29],used:[2,4,6,7,11,12,13,15,17,18,22,23,24,26,28,29,30,31,32],useful:24,user:[7,31],uses:[24,28],using:[4,5,7,9,10,11,12,13,17,18,21,22,23,26,27,28],usual:[9,15],utm_campaign:27,utm_medium:27,utm_sourc:27,val:24,valid:[10,22],valu:[4,6,9,17,22,24,26,27,28,29,31,32],van:9,variabl:[6,28],varianc:[2,11],variat:21,varied_length:28,variou:21,vdwradii:9,vector:[1,2,4,5,11,15,18,21,26,28,30],vector_ar:28,vectorautoregress:28,vel:5,veloc:[5,7,13],verbos:9,veri:[15,32],version:[23,26],versu:[0,18,26],vertic:[2,11,12,26],via:[12,27],viabl:12,vinyl:[29,31],virtual:[29,32],virtual_sit:29,viscos:27,visual:[4,10,22],vmd:10,volum:[7,22],waal:9,wai:[6,15,28,31,32],want:[4,7,10,11,15,18,22,28,29,30],wast:12,water:[5,7,9,10,12,13,17,18,26],water_cont:26,wedg:[2,11,26],weight:[1,2,6,21,26,29,32],weight_perc:[1,2,26],well:[12,13,15,30],were:21,what:29,whatev:29,when:[2,15,17,18,22,23,26,30,31,32],where:[1,4,8,9,11,12,17,18,22,28,31],whether:[1,2,5,7,29,32],which:[1,2,4,6,7,8,9,10,11,12,13,15,17,18,21,22,23,24,26,27,28,29,30,31,32],whole:[4,26],whose:[15,18,22],why:15,wiesenau:12,wiggl:[4,10,22],within:[1,4,12,26,29,31],without:[29,31,32],word:28,work:[2,9,12,21,22,23,26,27,28,31,32],workaround:29,worth:17,would:[12,15,28],wrap:12,wrap_box:18,wrapper:14,write:[7,8,11,14,26,28],write_assembl:5,write_em_mdp:[5,7],write_final_pore_configur:26,write_gro:[5,11],write_gro_po:5,write_npt_mdp:7,write_nve_mdp:7,write_nvt_mdp:7,write_top:8,write_water_ndx:5,written:[5,7,8,13,17,32],wrote:6,wustl:21,www:[21,27,28],x_box:18,x_lower:4,x_upper:4,xlink:[5,7,8,13,15,29,31],xlink_schem:32,xlink_top_nam:31,xlink_topnam:8,xlinked_top_nam:8,xlinkreact:32,xmin:[6,24],xtc:[4,10,22],xunda:12,xyregion:18,xyz:[5,18,26,30,31],y1_t:[],y2_t:[],y_1:[],y_2:[],y_box:18,y_k:[],y_lower:4,y_t:28,y_upper:4,yelk:12,yes:7,yield:[9,10],you:[4,7,10,11,12,17,18,23,26,28,29,30,32],youngwoo:12,your:12,z_correl:11,zbox:18,zero:[4,31],zeta:[6,24],zhou:12,zip:31,zmean:28},titles:["Post-Simulation Trajectory Analysis","Build Initial QI Phase Configurations","Build Initial Configurations","Calculate Coordination Numbers","Correlation Functions","Read and Write Files","Fitting Functions","Generate Gromacs .mdp Files","Generate Gromacs Topology File","Gromacs Wrappers","Identify Hydrogen Bonds","Build Initial HII Phase Configurations","Simulate Lyotropic Liquid Crystal Membranes","Generate Gromacs Input Files","Useful Functions","Preparation of Liquid Crystal Monomers","Calculate Mean Squared Displacement","Distance Between Pores","Physical Properties","Place Solutes in Pores","Preparation of Monomers and Solutes","Generate Random Numbers","Radial Distribution Functions","Software Requirements","Randomly Sample Distributions","System Setup","Solvate an Initial Configuration","Statistical Analysis","Time Series Analysis","Get Topological Information","Coordinate Transformations","Cross-linking","Designing Cross-Linking Reactions","Plot z-coordinate Versus Radial Position"],titleterms:{"class":[1,4,7,8,10,11,18,22,26,27,28,29,31,32],"function":[4,5,6,7,8,9,10,11,13,14,17,18,21,22,24,26,27,28,29,30],"public":12,Useful:14,ambertool:23,analysi:[0,27,28],annot:15,argument:[2,4,7,8,10,13,17,22,26,31],background:12,between:17,bond:[10,15],build:[1,2,11],calcul:[3,16],cell:15,command:[4,7,8,10,13,22,26],configur:[1,2,11,26],construct:15,content:12,coordin:[3,30,33],correl:4,cross:[15,31,32],crystal:[12,15],design:32,displac:16,distanc:17,distribut:[22,24],effect:12,exampl:[4,10,22,26],file:[5,7,8,13],fit:6,gener:[7,8,13,21],get:29,gromac:[7,8,9,13,23],hii:11,hydrogen:[10,15],identifi:10,indic:12,inform:29,initi:[1,2,11,26],input:13,line:[4,7,8,10,13,22,26],link:[15,31,32],liquid:[12,15],lyotrop:12,mdp:7,mean:16,membran:12,monom:[15,20],name:[2,4,7,8,10,13,17,22,26,31],number:[3,21],phase:[1,11],physic:18,place:19,plot:33,pore:[17,19],posit:33,post:0,prepar:[15,20],properti:18,python:23,radial:[22,33],random:21,randomli:24,reaction:32,read:5,refer:12,repositori:12,requir:23,sampl:24,seri:28,setup:25,simul:[0,12],softwar:23,solut:[19,20],solvat:26,squar:16,statist:27,sub:[],summari:15,system:25,tabl:12,thi:12,time:28,topolog:[8,29],trajectori:0,transform:30,unit:15,usag:[4,10,22],use:12,versu:33,wrapper:9,write:5,z_correl:[]}})