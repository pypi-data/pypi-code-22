#!/usr/bin/env python 3
from accessoryFunctions.accessoryFunctions import MetadataObject, GenObject, printtime, make_path, write_to_logfile, \
    run_subprocess
from sipprCommon.objectprep import Objectprep
from sipprCommon.sippingmethods import Sippr
from Bio.Blast.Applications import NcbiblastnCommandline
import Bio.Application
from Bio import SeqIO
from threading import Thread
from subprocess import PIPE
from csv import DictReader
from glob import glob
import operator
import time
import os

__author__ = 'adamkoziol'


class SixteenSBait(Sippr):

    def main(self):
        """

        """
        self.targets()
        self.bait()
        self.reversebait()
        self.subsample_reads()

    def targets(self):
        """
        Create the GenObject for the analysis type, create the hash file for baiting (if necessary)
        """
        for sample in self.runmetadata:
            if sample.general.bestassemblyfile != 'NA':
                setattr(sample, self.analysistype, GenObject())
                sample[self.analysistype].runanalysis = True
                sample[self.analysistype].targetpath = self.targetpath
                baitpath = os.path.join(self.targetpath, 'bait')
                sample[self.analysistype].baitfile = glob(os.path.join(baitpath, '*.fa'))[0]
                sample[self.analysistype].outputdir = os.path.join(sample.run.outputdirectory, self.analysistype)
                sample[self.analysistype].logout = os.path.join(sample[self.analysistype].outputdir, 'logout.txt')
                sample[self.analysistype].logerr = os.path.join(sample[self.analysistype].outputdir, 'logerr.txt')
                sample[self.analysistype].baitedfastq = \
                    '{}/{}_targetMatches.fastq'.format(sample[self.analysistype].outputdir, self.analysistype)
                sample[self.analysistype].complete = False

    def bait(self):
        """
        Use bbduk to perform baiting
        """
        printtime('Performing kmer baiting of fastq files with {} targets'.format(self.analysistype), self.start,
                  output=self.portallog)
        for sample in self.runmetadata:
            if sample.general.bestassemblyfile != 'NA':
                # Create the folder (if necessary)
                make_path(sample[self.analysistype].outputdir)
                # Make the system call
                if len(sample.general.fastqfiles) == 2:
                    # Create the command to run the baiting - paired inputs and a single, zipped output
                    sample[self.analysistype].bbdukcmd = \
                        'bbduk.sh ref={} in1={} in2={} k=51 mincovfraction=0.5 threads={} outm={}' \
                        .format(sample[self.analysistype].baitfile,
                                sample.general.trimmedcorrectedfastqfiles[0],
                                sample.general.trimmedcorrectedfastqfiles[1],
                                str(self.threads),
                                sample[self.analysistype].baitedfastq)
                else:
                    sample[self.analysistype].bbdukcmd = 'bbduk.sh ref={} in={} threads={} outm={}' \
                        .format(sample[self.analysistype].baitfile,
                                sample.general.trimmedcorrectedfastqfiles[0],
                                str(self.threads),
                                sample[self.analysistype].baitedfastq)
                # Run the system call (if necessary) , stdout=self.devnull, stderr=self.devnull
                if not os.path.isfile(sample[self.analysistype].baitedfastq):
                    # call(sample[self.analysistype].bbdukcmd, shell=True)
                    out, err = run_subprocess(sample[self.analysistype].bbdukcmd)
                    write_to_logfile(sample[self.analysistype].bbdukcmd,
                                     sample[self.analysistype].bbdukcmd,
                                     self.logfile, sample.general.logout, sample.general.logerr,
                                     sample[self.analysistype].logout, sample[self.analysistype].logerr)
                    write_to_logfile(out,
                                     err,
                                     self.logfile, sample.general.logout, sample.general.logerr,
                                     sample[self.analysistype].logout, sample[self.analysistype].logerr)

    def reversebait(self):
        """
        Use the baited FASTQ files to bait out the targets from the database to create a (hopefully) smaller
        database to use for the reference mapping step
        """
        printtime('Performing reverse kmer baiting of targets with fastq files', self.start, output=self.portallog)
        for sample in self.runmetadata:
            if sample.general.bestassemblyfile != 'NA':
                outfile = os.path.join(sample[self.analysistype].outputdir, 'baitedtargets.fa')
                sample[self.analysistype].revbbdukcmd = \
                    'bbduk.sh ref={} in={} threads={} mincovfraction={} maskmiddle=f outm={}'\
                    .format(sample[self.analysistype].baitedfastq,
                            sample[self.analysistype].baitfile,
                            str(self.threads),
                            self.cutoff,
                            outfile)
                # Run the system call (if necessary) , stdout=self.devnull, stderr=self.devnull
                if not os.path.isfile(outfile):
                    # call(sample[self.analysistype].revbbdukcmd, shell=True)
                    out, err = run_subprocess(sample[self.analysistype].revbbdukcmd)
                    write_to_logfile(sample[self.analysistype].bbdukcmd,
                                     sample[self.analysistype].bbdukcmd,
                                     self.logfile, sample.general.logout, sample.general.logerr,
                                     sample[self.analysistype].logout, sample[self.analysistype].logerr)
                    write_to_logfile(out,
                                     err,
                                     self.logfile, sample.general.logout, sample.general.logerr,
                                     sample[self.analysistype].logout, sample[self.analysistype].logerr)
                # Set the baitfile to use in the mapping steps as the newly created outfile
                sample[self.analysistype].baitfile = outfile

    def subsample_reads(self):
        """
        Subsampling of reads to 20X coverage of rMLST genes (roughly).
        To be called after rMLST extraction and read trimming, in that order.
        """
        printtime('Subsampling {} reads'.format(self.analysistype), self.start, output=self.portallog)
        for sample in self.runmetadata:
            # Create the name of the subsampled read file
            sample[self.analysistype].subsampledreads = os.path.join(
                sample[self.analysistype].outputdir, '{}_targetMatches_subsampled.fastq.gz'.format(self.analysistype))
            # Set the reformat.sh command - as this command will be run multiple times, overwrite previous iterations
            # each time. Use samplebasestarget to provide an approximation of the number of bases to include in the
            # subsampled reads e.g. for rMLST: 700000 (approx. 35000 bp total length of genes x 20X coverage)
            sample[self.analysistype].subsamplecmd = 'reformat.sh in={} out={} overwrite samplebasestarget=700000' \
                .format(sample[self.analysistype].baitedfastq,
                        sample[self.analysistype].subsampledreads)
            if not os.path.isfile(sample[self.analysistype].subsampledreads):
                # Run the call
                # call(sample[self.analysistype].subsamplecmd, shell=True, stdout=self.devnull, stderr=self.devnull)
                out, err = run_subprocess(sample[self.analysistype].subsamplecmd)
                write_to_logfile(sample[self.analysistype].subsamplecmd,
                                 sample[self.analysistype].subsamplecmd,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
                write_to_logfile(out,
                                 err,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
            # Update the variable to store the baited reads
            sample[self.analysistype].baitedfastq = sample[self.analysistype].subsampledreads


class SixteenSSipper(Sippr):

    def main(self):
        """

        """
        self.targets()
        self.bait()
        # If desired, use bbduk to bait the target sequences with the previously baited FASTQ files
        if self.revbait:
            self.reversebait()
        # Run the bowtie2 read mapping module
        self.mapping()
        # Use samtools to index the sorted bam file
        self.indexing()
        # Parse the results
        self.parsing()
        # Clear out the large attributes that will difficult to handle objects
        self.clear()
        # Filter out any sequences with cigar features such as internal soft-clipping from the results
        self.clipper()

    def targets(self):
        """
        Using the data from the BLAST analyses, set the targets folder, and create the 'mapping file'. This is the
        genera-specific FASTA file that will be used for all the reference mapping; it replaces the 'bait file' in the
        code
        """
        printtime('Performing analysis with {} targets folder'.format(self.analysistype), self.start,
                  output=self.portallog)
        for sample in self.runmetadata:
            if sample.general.bestassemblyfile != 'NA':
                sample[self.analysistype].targetpath = \
                    os.path.join(self.targetpath, 'genera', sample[self.analysistype].genus, '')
                # There is a relatively strict databasing scheme necessary for the custom targets. Eventually,
                # there will be a helper script to combine individual files into a properly formatted combined file
                try:
                    sample[self.analysistype].mappingfile = glob('{}*.fa'
                                                                 .format(sample[self.analysistype].targetpath))[0]
                # If the fasta file is missing, raise a custom error
                except IndexError as e:
                    # noinspection PyPropertyAccess
                    e.args = ['Cannot find the combined fasta file in {}. Please note that the file must have a '
                              '.fasta extension'.format(sample[self.analysistype].targetpath)]
                    if os.path.isdir(sample[self.analysistype].targetpath):
                        raise
                    else:
                        sample.general.bestassemblyfile = 'NA'


class SixteenS(object):

    def runner(self):
        """
        Run the necessary methods in the correct order
        """
        printtime('Starting {} analysis pipeline'.format(self.analysistype), self.starttime, output=self.portallog)
        if not self.pipeline:
            # If the metadata has been passed from the method script, self.pipeline must still be false in order to
            # get Sippr() to function correctly, but the metadata shouldn't be recreated
            try:
                _ = vars(self.runmetadata)['samples']
            except KeyError:
                # Create the objects to be used in the analyses
                objects = Objectprep(self)
                objects.objectprep()
                self.runmetadata = objects.samples

        else:
            for sample in self.runmetadata.samples:
                setattr(sample, self.analysistype, GenObject())
                sample.run.outputdirectory = sample.general.outputdirectory
        self.threads = int(self.cpus / len(self.runmetadata.samples)) \
            if self.cpus / len(self.runmetadata.samples) > 1 \
            else 1
        # Use a custom sippr method to use the full reference database as bait, and run mirabait against the FASTQ
        # reads - do not perform reference mapping yet
        SixteenSBait(self, self.cutoff)
        # Subsample 1000 reads from the FASTQ files
        self.subsample()
        # Convert the subsampled FASTQ files to FASTA format
        self.fasta()
        # Create BLAST databases if required
        self.makeblastdb()
        # Run BLAST analyses of the subsampled FASTA files against the NCBI 16S reference database
        self.blast()
        # Parse the BLAST results
        self.blastparse()
        # Feed the BLAST results into a modified sippr method to perform reference mapping using the calculated
        # genus of the sample as the mapping file
        SixteenSSipper(self, self.cutoff)
        # Create reports
        self.reporter()

    def subsample(self):
        """
        Subsample 1000 reads from the baited files
        """
        # Create the threads for the analysis
        printtime('Subsampling FASTQ reads', self.starttime, output=self.portallog)
        for _ in range(self.cpus):
            threads = Thread(target=self.subsamplethreads, args=())
            threads.setDaemon(True)
            threads.start()
        for sample in self.runmetadata.samples:
            # Set the name of the subsampled FASTQ file
            sample[self.analysistype].subsampledfastq = os.path.splitext(sample[self.analysistype].baitedfastq)[0] \
                                                        + '_subsampled.fastq'
            # Set the system call
            sample[self.analysistype].seqtkcall = 'seqtk sample {} 1000 > {}'\
                .format(sample[self.analysistype].baitedfastq,
                        sample[self.analysistype].subsampledfastq)
            # Add the sample to the queue
            self.samplequeue.put(sample)
        self.samplequeue.join()

    def subsamplethreads(self):
        while True:
            sample = self.samplequeue.get()
            # Check to see if the subsampled FASTQ file has already been created
            if not os.path.isfile(sample[self.analysistype].subsampledfastq):
                # Run the system call
                # call(sample[self.analysistype].seqtkcall, shell=True, stdout=self.devnull, stderr=self.devnull)
                out, err = run_subprocess(sample[self.analysistype].seqtkcall)
                write_to_logfile(sample[self.analysistype].seqtkcall,
                                 sample[self.analysistype].seqtkcall,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
                write_to_logfile(out,
                                 err,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
            self.samplequeue.task_done()

    def fasta(self):
        """
        Convert the subsampled reads to FASTA format using fastq_to_fasta from the FASTX toolkit
        """
        printtime('Converting FASTQ files to FASTA format', self.starttime, output=self.portallog)
        # Create the threads for the analysis
        for _ in range(self.cpus):
            threads = Thread(target=self.fastathreads, args=())
            threads.setDaemon(True)
            threads.start()
        for sample in self.runmetadata.samples:
            # Set the name as the FASTA file - the same as the FASTQ, but with .fa file extension instead of .fastq
            sample[self.analysistype].fasta = os.path.splitext(sample[self.analysistype].subsampledfastq)[0] + '.fa'
            # Set the system call
            sample[self.analysistype].fastxcall = 'fastq_to_fasta -i {} -o {}'\
                .format(sample[self.analysistype].subsampledfastq, sample[self.analysistype].fasta)
            # Add the sample to the queue
            self.fastaqueue.put(sample)
        self.fastaqueue.join()

    def fastathreads(self):
        while True:
            sample = self.fastaqueue.get()
            # Check to see if the FASTA file already exists
            if not os.path.isfile(sample[self.analysistype].fasta):
                # Run the system call , stdout=self.devnull, stderr=self.devnull
                # call(sample[self.analysistype].fastxcall, shell=True)
                out, err = run_subprocess(sample[self.analysistype].fastxcall)
                write_to_logfile(sample[self.analysistype].fastxcall,
                                 sample[self.analysistype].fastxcall,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
                write_to_logfile(out,
                                 err,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
            self.fastaqueue.task_done()

    def makeblastdb(self):
        """
        Makes blast database files from targets as necessary
        """
        # Iterate through the samples to set the bait file.
        for sample in self.runmetadata.samples:
            # Remove the file extension
            db = os.path.splitext(sample[self.analysistype].baitfile)[0]
            # Add '.nhr' for searching below
            nhr = '{}.nhr'.format(db)
            # Check for already existing database files
            if not os.path.isfile(str(nhr)):
                # Create the databases
                command = 'makeblastdb -in {} -parse_seqids -max_file_sz 2GB -dbtype nucl -out {}'\
                    .format(sample[self.analysistype].baitfile, db)
                out, err = run_subprocess(command)
                write_to_logfile(command,
                                 command,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)
                write_to_logfile(out,
                                 err,
                                 self.logfile, sample.general.logout, sample.general.logerr,
                                 sample[self.analysistype].logout, sample[self.analysistype].logerr)

    def blast(self):
        """
        Run BLAST analyses of the subsampled FASTQ reads against the NCBI 16S reference database
        """
        printtime('BLASTing FASTA files against {} database'.format(self.analysistype), self.starttime,
                  output=self.portallog)
        for _ in range(self.cpus):
            threads = Thread(target=self.blastthreads, args=())
            threads.setDaemon(True)
            threads.start()
        for sample in self.runmetadata.samples:
            # Set the name of the BLAST report
            sample[self.analysistype].blastreport = os.path.join(
                sample[self.analysistype].outputdir, '{}_{}_blastresults.csv'.format(sample.name, self.analysistype))
            # Use the NCBI BLASTn command line wrapper module from BioPython to set the parameters of the search
            blastn = NcbiblastnCommandline(query=sample[self.analysistype].fasta,
                                           db=os.path.splitext(sample[self.analysistype].baitfile)[0],
                                           max_target_seqs=1,
                                           num_threads=12,
                                           outfmt="'6 qseqid sseqid positive mismatch gaps "
                                                  "evalue bitscore slen length qstart qend qseq sstart send sseq'",
                                           out=sample[self.analysistype].blastreport)
            # Add a string of the command to the metadata object
            sample[self.analysistype].blastcall = str(blastn)
            # Add the object and the command to the BLAST queue
            self.blastqueue.put((sample, blastn))
        self.blastqueue.join()

    def blastthreads(self):
        while True:
            sample, blastn = self.blastqueue.get()
            if not os.path.isfile(sample[self.analysistype].blastreport):
                # Ensure that the query file exists; this can happen with very small .fastq files
                if os.path.isfile(sample[self.analysistype].fasta):
                    # Perform the BLAST analysis
                    try:
                        blastn()
                    except Bio.Application.ApplicationError:
                       sample[self.analysistype].blastreport = str()
            self.blastqueue.task_done()

    def blastparse(self):
        """
        Parse the blast results, and store necessary data in dictionaries in sample object
        """
        printtime('Parsing BLAST results', self.starttime, output=self.portallog)
        # Load the NCBI 16S reference database as a dictionary
        # dbrecords = SeqIO.to_dict(SeqIO.parse(self.baitfile, 'fasta'))
        for sample in self.runmetadata.samples:
            # Load the NCBI 16S reference database as a dictionary
            dbrecords = SeqIO.to_dict(SeqIO.parse(sample[self.analysistype].baitfile, 'fasta'))
            # Allow for no BLAST results
            if os.path.isfile(sample[self.analysistype].blastreport):
                # Initialise a dictionary to store the number of times a genus is the best hit
                sample[self.analysistype].frequency = dict()
                # Open the sequence profile file as a dictionary
                blastdict = DictReader(open(sample[self.analysistype].blastreport),
                                       fieldnames=self.fieldnames, dialect='excel-tab')
                for record in blastdict:
                    # Create the subject id. It will look like this: gi|1018196593|ref|NR_136472.1|
                    subject = record['subject_id']
                    # Extract the genus name. Use the subject id as a key in the dictionary of the reference database.
                    # It will return the full record e.g. gi|1018196593|ref|NR_136472.1| Escherichia marmotae
                    # strain HT073016 16S ribosomal RNA, partial sequence
                    # This full description can be manipulated to extract the genus e.g. Escherichia
                    genus = dbrecords[subject].description.split('|')[-1].split()[0]
                    # Increment the number of times this genus was encountered, or initialise the dictionary with this
                    # genus the first time it is seen
                    try:
                        sample[self.analysistype].frequency[genus] += 1
                    except KeyError:
                        sample[self.analysistype].frequency[genus] = 1
                # Sort the dictionary based on the number of times a genus is seen
                sample[self.analysistype].sortedgenera = sorted(sample[self.analysistype].frequency.items(),
                                                                key=operator.itemgetter(1), reverse=True)
                try:
                    # Extract the top result, and set it as the genus of the sample
                    sample[self.analysistype].genus = sample[self.analysistype].sortedgenera[0][0]
                    # Previous code relies on having the closest refseq genus, so set this as above
                    sample.general.closestrefseqgenus = sample[self.analysistype].genus
                except IndexError:
                    # Populate attributes with 'NA'
                    sample[self.analysistype].sortedgenera = 'NA'
                    sample[self.analysistype].genus = 'NA'
                    sample.general.closestrefseqgenus = 'NA'
            else:
                # Populate attributes with 'NA'
                sample[self.analysistype].sortedgenera = 'NA'
                sample[self.analysistype].genus = 'NA'
                sample.general.closestrefseqgenus = 'NA'

    def reporter(self):
        """
        Creates a report of the results
        """
        from Bio.Seq import Seq
        from Bio.SeqRecord import SeqRecord
        from Bio.Alphabet import IUPAC
        # Create the path in which the reports are stored
        make_path(self.reportpath)
        # Initialise the header and data strings
        header = 'Strain,Gene,PercentIdentity,Genus,FoldCoverage\n'
        data = ''
        with open(os.path.join(self.reportpath, self.analysistype + '.csv'), 'w') as report:
            with open(os.path.join(self.reportpath, self.analysistype + '_sequences.fa'), 'w') as sequences:
                for sample in self.runmetadata.samples:
                    try:
                        # Select the best hit of all the full-length 16S genes mapped
                        sample[self.analysistype].besthit = sorted(sample[self.analysistype].results.items(),
                                                                   key=operator.itemgetter(1), reverse=True)[0][0]
                        # Add the sample name to the data string
                        data += sample.name + ','
                        # Find the record that matches the best hit, and extract the necessary values to be place in the
                        # data string
                        for name, identity in sample[self.analysistype].results.items():
                            if name == sample[self.analysistype].besthit:
                                data += '{},{},{},{}\n'.format(name, identity, sample[self.analysistype].genus,
                                                               sample[self.analysistype].avgdepth[name])
                                # Create a FASTA-formatted sequence output of the 16S sequence
                                record = SeqRecord(Seq(sample[self.analysistype].sequences[name],
                                                       IUPAC.unambiguous_dna),
                                                   id='{}_{}'.format(sample.name, '16S'),
                                                   description='')
                                SeqIO.write(record, sequences, 'fasta')
                    except (KeyError, IndexError):
                        data += '{}\n'.format(sample.name)
            # Write the results to the report
            report.write(header)
            report.write(data)

    def __init__(self, args, pipelinecommit, startingtime, scriptpath, analysistype, cutoff):
        """
        :param args: command line arguments
        :param pipelinecommit: pipeline commit or version
        :param startingtime: time the script was started
        :param scriptpath: home path of the script
        :param analysistype: name of the analysis being performed - allows the program to find databases
        :param cutoff: percent identity cutoff for matches
        """
        import multiprocessing
        from queue import Queue
        # Initialise variables
        self.commit = str(pipelinecommit)
        self.starttime = startingtime
        self.homepath = scriptpath
        self.analysistype = analysistype
        # Define variables based on supplied arguments
        self.path = os.path.join(args.path, '')
        assert os.path.isdir(self.path), u'Supplied path is not a valid directory {0!r:s}'.format(self.path)
        try:
            self.sequencepath = os.path.join(args.sequencepath, '')
        except AttributeError:
            self.sequencepath = self.path
        assert os.path.isdir(self.sequencepath), u'Sequence path  is not a valid directory {0!r:s}' \
            .format(self.sequencepath)
        try:
            self.targetpath = os.path.join(args.targetpath, self.analysistype, '')
        except AttributeError:
            self.targetpath = os.path.join(args.reffilepath, self.analysistype)
        try:
            self.reportpath = args.reportpath
        except AttributeError:
            self.reportpath = os.path.join(self.path, 'reports')
        assert os.path.isdir(self.targetpath), u'Target path is not a valid directory {0!r:s}' \
            .format(self.targetpath)
        try:
            self.bcltofastq = args.bcltofastq
        except AttributeError:
            self.bcltofastq = False
        self.miseqpath = args.miseqpath
        try:
            self.miseqfolder = args.miseqfolder
        except AttributeError:
            self.miseqfolder = str()
        try:
            self.portallog = args.portallog
        except AttributeError:
            self.portallog = os.path.join(self.path, 'portal.log')
        self.fastqdestination = args.fastqdestination
        self.logfile = args.logfile
        self.forwardlength = args.forwardlength
        self.reverselength = args.reverselength
        self.numreads = 2 if self.reverselength != 0 else 1
        self.customsamplesheet = args.customsamplesheet
        # Set the custom cutoff value
        self.cutoff = cutoff
        # Use the argument for the number of threads to use, or default to the number of cpus in the system
        self.cpus = int(args.cpus if args.cpus else multiprocessing.cpu_count())
        self.threads = int()
        self.runmetadata = args.runmetadata
        self.pipeline = args.pipeline
        try:
            self.copy = args.copy
        except AttributeError:
            self.copy = False
        self.revbait = True
        self.devnull = open(os.path.devnull, 'w')
        self.samplequeue = Queue(maxsize=self.cpus)
        self.fastaqueue = Queue(maxsize=self.cpus)
        self.blastqueue = Queue(maxsize=self.cpus)
        self.baitfile = str()
        self.taxonomy = {'Escherichia': 'coli', 'Listeria': 'monocytogenes', 'Salmonella': 'enterica'}
        # Fields used for custom outfmt 6 BLAST output:
        self.fieldnames = ['query_id', 'subject_id', 'positives', 'mismatches', 'gaps',
                           'evalue', 'bit_score', 'subject_length', 'alignment_length',
                           'query_start', 'query_end', 'query_sequence',
                           'subject_start', 'subject_end', 'subject_sequence']
        # Run the analyses
        self.runner()


if __name__ == '__main__':
    # Argument parser for user-inputted values, and a nifty help menu
    from argparse import ArgumentParser
    from subprocess import Popen
    # Get the current commit of the pipeline from git
    # Extract the path of the current script from the full path + file name
    homepath = os.path.split(os.path.abspath(__file__))[0]
    # Find the commit of the script by running a command to change to the directory containing the script and run
    # a git command to return the short version of the commit hash
    commit = Popen('cd {} && git rev-parse --short HEAD'.format(homepath),
                   shell=True, stdout=PIPE).communicate()[0].rstrip()
    # Parser for arguments
    parser = ArgumentParser(description='Perform modelling of parameters for GeneSipping')
    parser.add_argument('path',
                        help='Specify input directory')
    parser.add_argument('-s', '--sequencepath',
                        required=True,
                        help='Path of .fastq(.gz) files to process.')
    parser.add_argument('-t', '--targetpath',
                        required=True,
                        help='Path of target files to process.')
    parser.add_argument('-n', '--cpus',
                        help='Number of threads. Default is the number of cores in the system')
    parser.add_argument('-b', '--bcltofastq',
                        action='store_true',
                        help='Optionally run bcl2fastq on an in-progress Illumina MiSeq run. Must include:'
                             'miseqpath, and miseqfolder arguments, and optionally readlengthforward, '
                             'readlengthreverse, and projectName arguments.')
    parser.add_argument('-m', '--miseqpath',
                        help='Path of the folder containing MiSeq run data folder')
    parser.add_argument('-f', '--miseqfolder',
                        help='Name of the folder containing MiSeq run data')
    parser.add_argument('-d', '--fastqdestination',
                        help='Optional folder path to store .fastq files created using the fastqCreation module. '
                             'Defaults to path/miseqfolder')
    parser.add_argument('-r1', '--forwardlength',
                        default='full',
                        help='Length of forward reads to use. Can specify "full" to take the full length of '
                             'forward reads specified on the SampleSheet')
    parser.add_argument('-r2', '--reverselength',
                        default='full',
                        help='Length of reverse reads to use. Can specify "full" to take the full length of '
                             'reverse reads specified on the SampleSheet')
    parser.add_argument('-c', '--customsamplesheet',
                        help='Path of folder containing a custom sample sheet (still must be named "SampleSheet.csv")')
    parser.add_argument('-P', '--projectName',
                        help='A name for the analyses. If nothing is provided, then the "Sample_Project" field '
                             'in the provided sample sheet will be used. Please note that bcl2fastq creates '
                             'subfolders using the project name, so if multiple names are provided, the results '
                             'will be split as into multiple projects')
    parser.add_argument('-D', '--detailedReports',
                        action='store_true',
                        help='Provide detailed reports with percent identity and depth of coverage values '
                             'rather than just "+" for positive results')
    parser.add_argument('-u', '--cutoff',
                        default=0.8,
                        help='Custom cutoff values')
    parser.add_argument('-C', '--copy',
                        action='store_true',
                        help='Normally, the program will create symbolic links of the files into the sequence path, '
                             'however, the are occasions when it is necessary to copy the files instead')
    # Get the arguments into an object
    arguments = parser.parse_args()
    arguments.pipeline = False
    arguments.runmetadata.samples = MetadataObject()
    arguments.logfile = os.path.join(arguments.path, 'logfile')
    arguments.analysistype = 'sixteens_full'
    # Define the start time
    start = time.time()

    # Run the script
    SixteenS(arguments, commit, start, homepath, arguments.analysistype, arguments.cutoff)

    # Print a bold, green exit statement
    print('\033[92m' + '\033[1m' + "\nElapsed Time: %0.2f seconds" % (time.time() - start) + '\033[0m')
