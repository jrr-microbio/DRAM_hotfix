#!/usr/bin/env python3

import argparse

from mag_annotator.database_processing import prepare_databases, set_database_paths, print_database_locations,\
                                              populate_description_db, update_dram_forms

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    subparsers = parser.add_subparsers()
    prepare_dbs_parser = subparsers.add_parser('prepare_databases',
                                               help="Download and process databases for annotation",
                                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    set_db_locs_parser = subparsers.add_parser('set_database_locations',
                                               help="Set database locations for already processed databases",
                                               formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    update_description_db_parser = subparsers.add_parser('update_description_db', help='Update description database',
                                                         formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    update_dram_forms_parser = subparsers.add_parser('update_dram_forms',
                                                     help='Update DRAM distillate and liquor forms',
                                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    print_db_locs_parser = subparsers.add_parser('print_config', help="Print database locations",
                                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # parser for downloading and processing databases for annotation and summarization
    prepare_dbs_parser.add_argument('--output_dir', default=".", help="output directory")
    prepare_dbs_parser.add_argument('--kegg_loc', default=None,
                                    help="KEGG protein file, should be a single .pep, please merge all KEGG pep files")
    prepare_dbs_parser.add_argument('--gene_ko_link_loc', default=None,
                                    help="KEGG gene ko link, can be gzipped or not")
    prepare_dbs_parser.add_argument('--kegg_download_date', default=None,
                                    help="Date KEGG was download to include in database name")
    prepare_dbs_parser.add_argument('--uniref_loc', default=None, help="File path to uniref, if already downloaded")
    prepare_dbs_parser.add_argument('--uniref_version', default='90', help="UniRef version to download")
    prepare_dbs_parser.add_argument('--pfam_loc', default=None,
                                    help="File path to pfam-A hmm file, if already downloaded")
    prepare_dbs_parser.add_argument('--pfam_hmm_dat', default=None, help="pfam hmm .dat file to get PF"
                                                                         "descriptions, if already downloaded")
    prepare_dbs_parser.add_argument('--dbcan_loc', default=None, help="File path to dbCAN, if already downloaded")
    prepare_dbs_parser.add_argument('--dbcan_fam_activities', default=None, help='CAZY family activities file, if'
                                                                                 'already downloaded')
    prepare_dbs_parser.add_argument('--dbcan_version', default='8', type=str, help='version of dbCAN to use')
    prepare_dbs_parser.add_argument('--vogdb_loc', default=None, help='hmm file for vogdb, if already downloaded')
    prepare_dbs_parser.add_argument('--viral_loc', default=None,
                                    help="File path to viral protein faa, if already downloaded")
    prepare_dbs_parser.add_argument('--peptidase_loc', default=None,
                                    help="File path to MEROPS peptidase fasta, if already downloaded")
    prepare_dbs_parser.add_argument('--genome_summary_form_loc', default=None, help="File path to genome summary form,"
                                                                                    "if already downloaded")
    prepare_dbs_parser.add_argument('--module_step_form_loc', default=None, help="File path to module step form, if"
                                                                                 "already downloaded")
    prepare_dbs_parser.add_argument('--etc_module_database_loc', default=None,
                                    help="File path to etc module database, if already downloaded")
    prepare_dbs_parser.add_argument('--function_heatmap_form_loc', default=None,
                                    help="File path to function heatmap form, if already downloaded")
    prepare_dbs_parser.add_argument('--branch', default='master', help="git branch from which to download forms; THIS "
                                                                       "SHOULD NOT BE CHANGED BY REGULAR USERS")
    prepare_dbs_parser.add_argument('--keep_database_files', default=False, action='store_true',
                                    help="Keep unporcessed database files")
    prepare_dbs_parser.add_argument('--threads', default=10, type=int,
                                    help="Number of threads to use building mmseqs2 databases")
    prepare_dbs_parser.add_argument('--verbose', default=False, action='store_true', help="Make it talk more")
    prepare_dbs_parser.set_defaults(func=prepare_databases)

    # parser for setting database locations when you already have processed database files
    set_db_locs_parser.add_argument('--kegg_db_loc', default=None, help='mmseqs2 database file from kegg .pep file')
    set_db_locs_parser.add_argument('--uniref_db_loc', default=None, help='mmseqs2 database file from uniref .faa')
    set_db_locs_parser.add_argument('--pfam_db_loc', default=None, help='mmseqs2 database file from pfam .hmm')
    set_db_locs_parser.add_argument('--pfam_hmm_dat', default=None, help='pfam hmm .dat file to get PF descriptions')
    set_db_locs_parser.add_argument('--dbcan_db_loc', default=None,
                                    help='hmm file for dbcan, already processed with hmmpress')
    set_db_locs_parser.add_argument('--dbcan_fam_activities', default=None, help='CAZY family activities file')
    set_db_locs_parser.add_argument('--vogdb_db_loc', default=None,
                                    help='hmm file for vogdb, already processed with hmmpress')
    set_db_locs_parser.add_argument('--viral_db_loc', default=None,
                                    help='mmseqs2 database file from ref seq viral gene collection')
    set_db_locs_parser.add_argument('--peptidase_db_loc', default=None,
                                    help='mmseqs2 database file from MEROPS database')
    set_db_locs_parser.add_argument('--description_db_loc', default=None,
                                    help="Location to write description sqlite db")
    set_db_locs_parser.add_argument('--genome_summary_form_loc', default=None, help="File path to genome summary form")
    set_db_locs_parser.add_argument('--module_step_form_loc', default=None, help="File path to module step form")
    set_db_locs_parser.add_argument('--etc_module_database_loc', default=None, help="File path to etc module database")
    set_db_locs_parser.add_argument('--function_heatmap_form_loc', default=None,
                                    help="File path to function heatmap form")
    set_db_locs_parser.add_argument('--amg_database_loc', default=None, help="File path to amg database")
    set_db_locs_parser.add_argument('--update_description_db', action='store_true', default=False)
    set_db_locs_parser.set_defaults(func=set_database_paths)

    # parser for updating database descriptions
    update_description_db_parser.set_defaults(func=populate_description_db)

    # parser for updating DRAM databases only
    update_dram_forms_parser.add_argument('--output_dir', required=True,
                                          help="Directory to store newly downloaded files, may want this to be the same"
                                               " directory as the rest of your DRAM database files")
    update_dram_forms_parser.set_defaults(func=update_dram_forms)

    # parser for printing out database configuration information
    print_db_locs_parser.set_defaults(func=print_database_locations)

    args = parser.parse_args()
    args_dict = {i: j for i, j in vars(args).items() if i != 'func'}
    args.func(**args_dict)
