// Do NOT change. Changes will be lost next time file is generated

#define R__DICTIONARY_FILENAME dIUsersdIvaleriadamantedIDesktopdIDottoratodIpublicdICMSSW_11_2_0_pre9dIsrcdIValidationdImake_histogram_cpp_ACLiC_dict
#define R__NO_DEPRECATION

/*******************************************************************/
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#define G__DICTIONARY
#include "RConfig.h"
#include "TClass.h"
#include "TDictAttributeMap.h"
#include "TInterpreter.h"
#include "TROOT.h"
#include "TBuffer.h"
#include "TMemberInspector.h"
#include "TInterpreter.h"
#include "TVirtualMutex.h"
#include "TError.h"

#ifndef G__ROOT
#define G__ROOT
#endif

#include "RtypesImp.h"
#include "TIsAProxy.h"
#include "TFileMergeInfo.h"
#include <algorithm>
#include "TCollectionProxyInfo.h"
/*******************************************************************/

#include "TDataMember.h"

// The generated code does not explicitly qualifies STL entities
namespace std {} using namespace std;

// Header files passed as explicit arguments
#include "/Users/valeriadamante/Desktop/Dottorato/public/CMSSW_11_2_0_pre9/src/Validation/./make_histogram.cpp"

// Header files passed via #pragma extra_include

namespace {
  void TriggerDictionaryInitialization_make_histogram_cpp_ACLiC_dict_Impl() {
    static const char* headers[] = {
"./make_histogram.cpp",
0
    };
    static const char* includePaths[] = {
"/opt/local/libexec/root6/include/root",
"/opt/local/libexec/root6/etc/root",
"/opt/local/libexec/root6/etc/root/cling",
"/opt/local/libexec/root6/include/root",
"/opt/local/libexec/root6/include",
"/opt/local/var/macports/build/_opt_local_var_macports_sources_rsync.macports.org_macports_release_tarballs_ports_science_root6/root6/work/build/include",
"/opt/local/include",
"/opt/local/var/macports/build/_opt_local_var_macports_sources_rsync.macports.org_macports_release_tarballs_ports_science_root6/root6/work/build/include/",
"/opt/local/libexec/root6/include/root",
"/Users/valeriadamante/Desktop/Dottorato/public/CMSSW_11_2_0_pre9/src/Validation/",
0
    };
    static const char* fwdDeclCode = R"DICTFWDDCLS(
#line 1 "make_histogram_cpp_ACLiC_dict dictionary forward declarations' payload"
#pragma clang diagnostic ignored "-Wkeyword-compat"
#pragma clang diagnostic ignored "-Wignored-attributes"
#pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
extern int __Cling_AutoLoading_Map;
)DICTFWDDCLS";
    static const char* payloadCode = R"DICTPAYLOAD(
#line 1 "make_histogram_cpp_ACLiC_dict dictionary payload"

#ifndef __ACLIC__
  #define __ACLIC__ 1
#endif

#define _BACKWARD_BACKWARD_WARNING_H
// Inline headers
#include "./make_histogram.cpp"

#undef  _BACKWARD_BACKWARD_WARNING_H
)DICTPAYLOAD";
    static const char* classesHeaders[] = {
"SplitValueList", payloadCode, "@",
"color_list", payloadCode, "@",
"draw_histograms", payloadCode, "@",
"explore_paths", payloadCode, "@",
"file_to_write", payloadCode, "@",
"make_histogram", payloadCode, "@",
"opt_stat", payloadCode, "@",
nullptr
};
    static bool isInitialized = false;
    if (!isInitialized) {
      TROOT::RegisterModule("make_histogram_cpp_ACLiC_dict",
        headers, includePaths, payloadCode, fwdDeclCode,
        TriggerDictionaryInitialization_make_histogram_cpp_ACLiC_dict_Impl, {}, classesHeaders, /*hasCxxModule*/false);
      isInitialized = true;
    }
  }
  static struct DictInit {
    DictInit() {
      TriggerDictionaryInitialization_make_histogram_cpp_ACLiC_dict_Impl();
    }
  } __TheDictionaryInitializer;
}
void TriggerDictionaryInitialization_make_histogram_cpp_ACLiC_dict() {
  TriggerDictionaryInitialization_make_histogram_cpp_ACLiC_dict_Impl();
}
