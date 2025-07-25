# SuperLIM tasks
from __future__ import annotations

from mteb.abstasks.AbsTaskClassification import AbsTaskClassification
from mteb.abstasks.TaskMetadata import TaskMetadata


class DalajClassification(AbsTaskClassification):
    superseded_by = "DalajClassification.v2"
    metadata = TaskMetadata(
        name="DalajClassification",
        dataset={
            "path": "AI-Sweden/SuperLim",
            "revision": "7ebf0b4caa7b2ae39698a889de782c09e6f5ee56",
            "name": "dalaj",
            "trust_remote_code": True,
        },
        description="A Swedish dataset for linguistic acceptability. Available as a part of Superlim.",
        reference="https://spraakbanken.gu.se/en/resources/superlim",
        type="Classification",
        category="s2s",
        modalities=["text"],
        eval_splits=["test"],
        eval_langs=["swe-Latn"],
        main_score="accuracy",
        date=("2017-01-01", "2020-12-31"),
        domains=["Non-fiction", "Written"],
        task_subtypes=["Linguistic acceptability"],
        license="cc-by-4.0",
        annotations_creators="expert-annotated",
        dialect=[],
        sample_creation="created",
        bibtex_citation=r"""
@misc{2105.06681,
  author = {Elena Volodina and Yousuf Ali Mohammed and Julia Klezl},
  eprint = {arXiv:2105.06681},
  title = {DaLAJ - a dataset for linguistic acceptability judgments for Swedish: Format, baseline, sharing},
  year = {2021},
}
""",
        prompt="Classify texts based on linguistic acceptability in Swedish",
    )

    samples_per_label = 16

    def dataset_transform(self):
        """This dataset consist of two columns of relevance, "original_sentence" and "corrected_sentence".
        We will use the original sentence as we "wrong" sentence and the corrected sentence as the "correct" sentence
        """

        def __convert_sample_to_classification(sample):
            text = sample["original_sentence"] + sample["corrected_sentence"]
            label = [1] * len(sample["original_sentence"]) + [0] * len(
                sample["corrected_sentence"]
            )
            return {"text": text, "label": label}

        columns_to_keep = ["original_sentence", "corrected_sentence"]
        for split in self.dataset:
            columns_names = self.dataset[split].column_names  # type: ignore
            columns_to_remove = [
                col for col in columns_names if col not in columns_to_keep
            ]
            self.dataset[split] = self.dataset[split].remove_columns(columns_to_remove)  # type: ignore

        self.dataset = self.dataset.map(
            __convert_sample_to_classification,
            batched=True,
            remove_columns=columns_to_keep,
        )


class DalajClassificationV2(AbsTaskClassification):
    metadata = TaskMetadata(
        name="DalajClassification.v2",
        dataset={
            "path": "mteb/dalaj",
            "revision": "ecf6f2d83e8e85816ec3974896557a4aafce4f3e",
            "name": "dalaj",
        },
        description="""A Swedish dataset for linguistic acceptability. Available as a part of Superlim.
        This version corrects errors found in the original data. For details, see [pull request](https://github.com/embeddings-benchmark/mteb/pull/2900)""",
        reference="https://spraakbanken.gu.se/en/resources/superlim",
        type="Classification",
        category="s2s",
        modalities=["text"],
        eval_splits=["test"],
        eval_langs=["swe-Latn"],
        main_score="accuracy",
        date=("2017-01-01", "2020-12-31"),
        domains=["Non-fiction", "Written"],
        task_subtypes=["Linguistic acceptability"],
        license="cc-by-4.0",
        annotations_creators="expert-annotated",
        dialect=[],
        sample_creation="created",
        bibtex_citation=r"""
@misc{2105.06681,
  author = {Elena Volodina and Yousuf Ali Mohammed and Julia Klezl},
  eprint = {arXiv:2105.06681},
  title = {DaLAJ - a dataset for linguistic acceptability judgments for Swedish: Format, baseline, sharing},
  year = {2021},
}
""",
        prompt="Classify texts based on linguistic acceptability in Swedish",
        adapted_from=["DalajClassification"],
    )

    samples_per_label = 16
